"""El sello no depende del sistema: un clon de Windows (CRLF) verifica igual."""
from nelli import integridad


def test_sello_sobrevive_crlf(tmp_path):
    (tmp_path / "paquete-mx").mkdir()
    (tmp_path / "skills").mkdir()
    (tmp_path / "src" / "nelli" / "esquema").mkdir(parents=True)
    (tmp_path / "paquete-mx" / "a.json").write_bytes(b'{"a": 1}\n')
    (tmp_path / "skills" / "leer-v1.md").write_bytes(b"prompt\n")
    (tmp_path / "src" / "nelli" / "esquema" / "leer-v1.json").write_bytes(b"{}\n")
    integridad.sellar(tmp_path)
    for p in tmp_path.rglob("*"):
        if p.is_file() and p.name != "SHA256SUMS":
            p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    integridad.verificar(tmp_path)  # no debe lanzar
