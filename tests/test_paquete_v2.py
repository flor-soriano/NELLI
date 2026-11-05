"""Paquete MX v2: «nunca» verificados confirman; pendientes no. Sin red ni IA."""
from nelli.herramientas import lista_oficial
from nelli.nelli import Entrada, verificar


def v(texto, canal="sms"):
    return verificar(Entrada(texto=texto, canal=canal), con_ia=False, red=False)


def test_lista_v2_tiene_las_78_instituciones():
    filas = lista_oficial.cargar()["filas"]
    assert len(filas) >= 78
    bbva = next(f for f in filas if f["institucion"] == "BBVA México")
    assert bbva["verificado"] is True


def test_nunca_verificado_de_banco_confirma():
    # BBVA publica que nunca pide NIP/CVV por mensaje (fuente verificada 27-oct).
    t = v("BBVA: tu tarjeta fue bloqueada. Confirma tu NIP y CVV en el enlace que te enviamos.")
    assert t["nivel"] == "fraude_confirmado"


def test_banregio_pendiente_no_confirma():
    # Banregio quedó pendiente de revisión humana (resguardo armado): no confirma.
    t = v("Banregio: confirma tu contraseña y claves en la liga de este mensaje.")
    assert t["nivel"] != "fraude_confirmado"


def test_multa_falsa_es_muy_probable():
    t = v("Gobierno CDMX: tienes una multa de transito por $1,850. Paga hoy mismo para evitar el corralon: finanzas-cdmx-pagos.com")
    # La liga imita a la Tesorería CDMX (fila verificada): confirma por imitación.
    assert t["nivel"] == "fraude_confirmado"
    assert t["tipo"] == "multa_falsa"


def test_soporte_falso_no_es_otro():
    t = v("Apple Support: tu cuenta de Apple fue suspendida. Ingresa tu contrasena y codigo de verificacion para reactivarla.")
    assert t["tipo"] == "soporte_falso"
    assert t["nivel"] in ("posible_fraude", "muy_probablemente_fraude", "fraude_confirmado")
