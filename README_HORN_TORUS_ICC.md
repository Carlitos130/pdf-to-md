# Modelo 3D del Horn Torus del Icc

Programa para modelar y visualizar el **Horn Torus del Icc** (Inconsciente) integrando resultados del test psicométrico **SCL-90-R de Derogatis** con las variables:
- **S** (Significante)
- **I** (Imagen del cuerpo) 
- **Σ** (Síntoma)
- **Fantasía** como punto de angustia

## 📋 Descripción del Modelo

Este modelo representa cómo la **angustia** (asociada a la fantasía) puede romper la división **Pcc-Cc-Icc** en la locura, utilizando el **horn torus** como superficie base.

### Conceptos Clave:
- **Horn Torus**: Superficie con autotangencia en (0,0,0) que representa el Icc
- **S, I, Σ**: Curvas entrelazadas sobre la superficie que representan el significante, imagen del cuerpo y síntoma
- **Fantasía**: Punto de angustia máxima (u_F, v_F) = (π, π/2)
- **Rupturas**: Zonas donde A(u,v) > A_cr (umbral de angustia), simbolizando la pérdida de la división Pcc-Cc-Icc

## 🚀 Requisitos

```bash
pip install numpy matplotlib
```

## 📂 Archivos

- `horn_torus_icc_model.py` - Código principal del modelo
- `README_HORN_TORUS_ICC.md` - Este archivo de documentación

## 🎯 Uso

### 1. Ejecutar con datos de ejemplo

```bash
python horn_torus_icc_model.py
```

Esto generará:
- Visualización del modelo normal con curvas y rupturas
- Visualización del modelo deformado (locura)
- Archivos PNG guardados: `horn_torus_icc_normal.png` y `horn_torus_icc_deformed.png`

### 2. Usar con datos reales del SCL-90-R

```python
from horn_torus_icc_model import HornTorusICCModel

# Datos del SCL-90-R (valores normalizados entre 0 y 1)
scl90r_data = {
    "Somatización": 0.75,
    "Obsesión-Compulsión": 0.85,
    "Sensibilidad Interpersonal": 0.65,
    "Depresión": 0.90,
    "Ansiedad": 0.95,
    "Hostilidad": 0.70,
    "Ansiedad Fóbica": 0.80,
    "Ideación Paranoide": 0.75,
    "Psicoticismo": 0.95,
    "GSI": 0.90,    # Global Severity Index
    "PST": 0.80,    # Positive Symptom Total
    "PSDI": 0.95    # Positive Symptom Distress Index
}

# Crear modelo
model = HornTorusICCModel(scl90r_data=scl90r_data, a_scale=0.1)

# Imprimir resumen
model.print_model_summary()

# Visualizar modelo normal
model.plot_3d_model(
    show_ruptures=True,
    show_curves=True,
    save_path='mi_modelo_normal.png'
)

# Visualizar modelo deformado (locura)
model.plot_deformed_model(
    deformation_factor=0.3,
    save_path='mi_modelo_deformado.png'
)
```

## 🔧 Parámetros Configurables

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|------------------|
| `a_scale` | Factor de escala para el radio (a = a_scale × GSI) | 0.1 |
| `u_scale` | Factor de escala para parámetro u | 2π |
| `v_scale` | Factor de escala para parámetro v | π |
| `A_cr` | Umbral de angustia para rupturas | π/4 |
| `deformation_factor` | Factor de deformación en modelo de locura | 0.2 |

## 📊 Interpretación de la Visualización

### Modelo Normal:
- **Superficie azul claro**: Horn torus del Icc
- **Color de la superficie**: Gradiente según nivel de angustia A(u,v)
- **Curva roja (S)**: Significante
- **Curva verde (I)**: Imagen del cuerpo
- **Curva azul (Σ)**: Síntoma
- **Punto negro**: Fantasía (punto de angustia máxima)
- **Puntos morados**: Zonas de ruptura (A > A_cr)

### Modelo Deformado (Locura):
- **Superficie naranja**: Horn torus deformado
- **Curvas deformadas**: S, I, Σ con deformaciones locales
- **Puntos morados**: Rupturas con deformación aplicada

## 📈 Mapeo de Variables

### Radio `a`:
```
a = a_scale × GSI
```
Donde GSI (Global Severity Index) representa la gravedad global de los síntomas.

### Parámetro `u` (longitudinal):
- **S (Significante)**: Basado en Ansiedad y Obsesión-Compulsión
- **I (Imagen)**: Basado en Somatización y Sensibilidad Interpersonal
- **Σ (Síntoma)**: Basado en Psicoticismo y Hostilidad

### Parámetro `v` (latitudinal):
- **S**: Basado en PSDI (Positive Symptom Distress Index)
- **I**: Basado en PST (Positive Symptom Total)
- **Σ**: Basado en Psicoticismo

### Función de Angustia:
```
A(u, v) = √[(u - u_F)² + (v - v_F)²]
```
Donde (u_F, v_F) = (π, π/2) es el punto de fantasía.

## 🎨 Personalización

### Cambiar el umbral de angustia:
```python
model.A_cr = np.pi / 3  # Umbral más bajo
```

### Cambiar el punto de fantasía:
```python
model.fantasy_point = (np.pi/2, np.pi/2)  # Nuevo punto
```

### Cambiar colores:
Modificar en el método `get_curves()`:
```python
return {
    'S': {'x': x_S, 'y': y_S, 'z': z_S, 'color': 'darkred', ...},
    'I': {'x': x_I, 'y': y_I, 'z': z_I, 'color': 'darkgreen', ...},
    'Σ': {'x': x_Sigma, 'y': y_Sigma, 'z': z_Sigma, 'color': 'darkblue', ...}
}
```

## 📚 Referencias Matemáticas

### Ecuaciones del Horn Torus:
```
x(u, v) = a(1 + cos v) cos u
y(u, v) = a(1 + cos v) sin u
z(u, v) = a sin v
```

Donde:
- `a` = radio del tubo = radio de revolución (R = r = a)
- `u ∈ [0, 2π)`: Ángulo de revolución (longitudinal)
- `v ∈ [0, 2π)`: Ángulo de la sección transversal (latitudinal)

### Ecuación Implícita:
```
(√(x² + y²) - a)² + z² = a²
```

### Propiedades Geométricas:
- **Género**: 1 (como cualquier toro)
- **Superficie**: No regular en (0, 0, 0) (punto de autotangencia)
- **Área**: S = 4π²a²
- **Volumen**: V = 2π²a³

## 🔬 Aplicación Clínica

Este modelo permite:
1. **Visualizar** la estructura del Icc como superficie geométrica
2. **Identificar** zonas de tensión (angustia) en el inconsciente
3. **Modelar** la ruptura de la división Pcc-Cc-Icc en la locura
4. **Comparar** diferentes pacientes mediante sus horn torus
5. **Analizar** la evolución temporal de la estructura del Icc

## 📖 Ejemplo de Interpretación

Con los datos de ejemplo:
- **GSI = 0.85** → Radio a = 0.085
- **Punto de fantasía** en (π, π/2)
- **Umbral A_cr = π/4 ≈ 0.785**

Si en un punto (u, v) = (0.4π, 1.8π):
- A(u, v) ≈ 1.45π > A_cr
- **Interpretación**: Este punto supera el umbral de angustia, indicando una **ruptura local** en la división Pcc-Cc-Icc

## 🎯 Posibles Extensiones

1. **Dinámica temporal**: Animar cómo evoluciona el horn torus con el tiempo
2. **Comparación entre pacientes**: Superponer varios horn torus en una misma gráfica
3. **Análisis cuantitativo**: Calcular volumen o área de las zonas de ruptura
4. **Integración con otros tests**: Incorporar datos de otros tests psicométricos
5. **Realidad virtual**: Visualización inmersiva del modelo

## 📝 Notas

- Los valores del SCL-90-R deben estar **normalizados entre 0 y 1**
- El factor `a_scale` permite ajustar el tamaño de la visualización
- El `deformation_factor` controla la intensidad de la deformación en el modelo de locura
- Para mejores resultados, usar al menos 100 puntos de resolución en u y v

---

**Autor**: Modelo basado en la teoría del Horn Torus aplicada al psicoanálisis
**Versión**: 1.0
**Fecha**: 2024
