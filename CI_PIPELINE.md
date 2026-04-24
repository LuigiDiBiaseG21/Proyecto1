# CI Pipeline - AWS CodeBuild y AWS CodePipeline

Este repositorio está preparado para integración continua usando AWS CodeBuild y CodePipeline.
La rama principal de CI es `master`.

## Archivos importantes

- `buildspec.yml`: configuración de build que AWS CodeBuild usa para instalar dependencias, ejecutar pruebas y generar el artefacto.
- `README.md`: documentación de ejecución local y de CI.
- `tests/test_blacklist.py`: pruebas unitarias que se ejecutan en el pipeline.

## Configuración recomendada de AWS CodeBuild

1. **Nombre del proyecto**: `proyecto1-codebuild`
2. **Source**: GitHub
   - Repositorio: `LuigiDiBiaseG21/Proyecto1`
   - Branch: `master`
3. **Entorno**:
   - Managed image
   - `aws/codebuild/standard:8.0` o equivalente
   - Runtime: `Python 3.12`
4. **Buildspec**:
   - Usar `buildspec.yml` en la raíz del proyecto
5. **Artifacts**:
   - Tipo: `Amazon S3` (si CodeBuild se usa fuera de un pipeline) o dejar que CodePipeline maneje los artifacts.
   - El archivo generado es `blacklist-app.zip`.

## Contenido de buildspec.yml

El archivo define las siguientes fases:

- `install`
  - Actualiza pip
  - Instala dependencias del proyecto
- `pre_build`
  - Ejecuta las pruebas unitarias con `pytest`
- `build`
  - Empaqueta la aplicación en `blacklist-app.zip`
- `post_build`
  - Registra la finalización de la build

El artefacto generado se usa solo como evidencia de construcción, no para despliegue.

## Configuración recomendada de AWS CodePipeline

1. **Nombre del pipeline**: `proyecto1-ci-pipeline`
2. **Stage Source**:
   - Source provider: GitHub
   - Repository: `LuigiDiBiaseG21/Proyecto1`
   - Branch: `master`
   - Change detection: habilitada
3. **Stage Build**:
   - Build provider: AWS CodeBuild
   - Project: `proyecto1-codebuild`
4. **No agregar stage de despliegue**:
   - Esta entrega es de CI únicamente. No implementar CD.

## Flujo de validación local

Para emular el pipeline en tu equipo:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
```

## Cómo generar un pipeline exitoso

1. Asegúrate de que tu código está en `master`.
2. Ejecuta localmente `python -m pytest -q`.
3. Haz commit y push.
4. El pipeline se activará automáticamente y debe terminar como `Succeeded`.

## Cómo generar un pipeline fallido

1. Introduce un cambio temporal que rompa una prueba o cause un error de sintaxis.
2. Haz commit y push a `master`.
3. El pipeline debe fallar en la etapa de CodeBuild.

## Evidencias para la entrega

Captura y documenta:

- Nombre del proyecto CodeBuild
- Nombre del pipeline CodePipeline
- Branch utilizado: `master`
- Logs de CodeBuild con pruebas exitosas
- Logs de CodeBuild con pruebas fallidas
- Pantalla del pipeline en estado `Succeeded` y `Failed`
