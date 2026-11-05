# eval/

- `correr.py`: corre los casos contra Nelli (reglas + Spark) o contra reglas solas (`--sin-ia`) e imprime los dos errores con intervalo de Wilson 95 %.
- El corpus grande del plan (~600 casos con 30 % ciego) no se alcanzó a construir. La prueba que sí se corrió (3-nov-2026) usa `eval/casos-documentados-50.jsonl`: 50 casos documentados el 31-oct desde alertas públicas, posteriores a las reglas v2 (28-oct), corridos una vez por rival con `correr.py`. Resultados en el README, sección «Resultados».
- Rivales: (1) reglas solas (`correr.py --sin-ia`) · (2) Nelli completa (`correr.py`) · (3) Spark solo, tomando su `nivel_sugerido` tal cual: se corrió a mano el 3-nov y no hay script en el repo que lo repita · (4) Bitdefender Scamio: no se corrió (es una prueba manual externa).
