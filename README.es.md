# Loxihart Ratchet

**Checkpoints pequeños. Evidencia antes de avanzar.**

Un componente reutilizable para agentes de programación, inspirado en el método Helix publicado por Shopify. Sirve para migraciones, refactors y funcionalidades que necesitan verificación incremental.

[English](README.md) · [Instalación](docs/installation.md) · [Método](docs/method.md) · [Ejemplo](examples/checkpoint-walkthrough.md)

Es una implementación independiente de la comunidad. No es la herramienta interna de Shopify ni un producto oficial de Shopify. El instalador, el registro de evidencia y los adaptadores pertenecen a este proyecto.

## Instalación rápida

Necesitas Python 3.10+; el registro opcional también necesita Git. No se requieren claves API ni dependencias Python para ejecutar el instalador o el registro.

```bash
git clone https://github.com/Krosebrook/loxihart-ratchet.git
cd loxihart-ratchet
python3 scripts/install.py --agent codex --project /ruta/absoluta/a/tu-proyecto
```

Abre tu agente dentro de **tu proyecto** y escribe:

> Usa Ratchet para implementar [cambio]. Empieza por el checkpoint verificable más pequeño. Presenta la evidencia y los controles pendientes antes de continuar.

Puedes sustituir `codex` por `claude`, `antigravity`, `gemini`, `grok`, `opencode`, `kimi`, `qwen` o `copilot`. Usa `--dry-run` para ver las rutas antes de copiar archivos. El instalador conserva la configuración existente y rechaza sobrescribir skills diferentes.

En Claude Code también puedes instalar el plugin:

```text
/plugin marketplace add Krosebrook/loxihart-ratchet
/plugin install loxihart-ratchet@loxihart-ratchet
```

Invocación: `/loxihart-ratchet:ratchet` como plugin de Claude; `$ratchet` en Codex; lenguaje natural en cualquier agente que pueda cargar las skills.

## Cómo funciona

1. Toma el software existente o los requisitos aceptados como referencia.
2. Define e implementa una porción pequeña, con criterios observables.
3. Demuestra su comportamiento mediante pruebas o verificaciones en ejecución.
4. Compara la interfaz cuando corresponde.
5. Obtén dos revisiones adversariales en sesiones independientes.
6. Presenta la evidencia al ingeniero; corrige y repite si hay hallazgos.
7. Cierra el checkpoint, realiza el commit cuando esté autorizado y conserva lo aprendido.

La aprobación humana es el valor predeterminado. Una delegación explícita y acotada permite avanzar dentro de ese alcance, manteniendo los controles técnicos. Si faltan herramientas o revisores, el control queda pendiente: el agente no puede inventar una aprobación.

## Qué incluye

| Skill | Función |
| --- | --- |
| `ratchet` | Coordina el ciclo y el registro de evidencia |
| `ratchet-plan` | Define checkpoints y criterios de aceptación |
| `ratchet-behavior` | Verifica comportamiento |
| `ratchet-ui-review` | Revisa paridad visual |
| `ratchet-adversarial-review` | Busca defectos y desviaciones de arquitectura |
| `ratchet-memory` | Conserva decisiones aceptadas y contexto de reanudación |

Además incluye un instalador por agente, manifiestos de plugin para Codex y Claude Code, plantillas, ejemplos, pruebas automatizadas y CI.

## Alcance real de la compatibilidad

Las rutas de instalación están documentadas para Codex, Claude Code, Antigravity, Gemini CLI, Grok Build, OpenCode, Kimi Code, Qwen Code y GitHub Copilot. Las pruebas locales verifican el instalador y el registro; **todavía no se han probado sesiones completas en los nueve agentes**. Consulta la [matriz de compatibilidad](docs/compatibility.md).

Las skills dependen de las herramientas del agente. No incluyen un simulador, un modelo visual, credenciales, un servicio MCP ni un proceso autónomo en segundo plano.

El registro detecta evidencia obsoleta, controles faltantes y sesiones declaradas como duplicadas. No autentica identidades ni demuestra por sí solo que una prueba o aprobación sea verdadera. Para exigir estas reglas fuera del agente, añade CI y protección de ramas.

## Probar el paquete

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Los datos de ejecución se guardan en `.ratchet/` dentro del proyecto de destino. Mantén esa carpeta fuera de Git y publica únicamente evidencia seleccionada y saneada.

Licencia MIT. [Fuentes y atribución](docs/sources.md).
