#!/usr/bin/env python3
"""
Modelo 3D del Horn Torus para el Icc (Inconsciente)
Integra resultados del test psicométrico SCL-90-R de Derogatis
con variables S (Significante), I (Imagen del cuerpo), Σ (Síntoma)
y la fantasía como punto de angustia.

Este modelo representa cómo la angustia (asociada a la fantasía) puede romper
la división Pcc-Cc-Icc en la locura, utilizando el horn torus como superficie base.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


class HornTorusICCModel:
    """
    Clase principal para modelar y visualizar el Horn Torus del Icc
    con datos del SCL-90-R.
    """
    
    def __init__(self, scl90r_data=None, a_scale=0.1, u_scale=2*np.pi, v_scale=np.pi):
        """
        Inicializa el modelo con datos del SCL-90-R.
        
        Args:
            scl90r_data (dict): Diccionario con resultados del SCL-90-R.
                              Ejemplo: {"GSI": 0.85, "PST": 0.7, "PSDI": 0.9, 
                                       "Somatización": 0.8, "Obsesión-Compulsión": 0.9, ...}
            a_scale (float): Factor de escala para el radio a (default: 0.1)
            u_scale (float): Factor de escala para el parámetro u (default: 2π)
            v_scale (float): Factor de escala para el parámetro v (default: π)
        """
        # Datos por defecto del SCL-90-R (valores normalizados entre 0 y 1)
        self.default_scl90r_data = {
            "Somatización": 0.8,
            "Obsesión-Compulsión": 0.9,
            "Sensibilidad Interpersonal": 0.7,
            "Depresión": 0.85,
            "Ansiedad": 0.95,
            "Hostilidad": 0.6,
            "Ansiedad Fóbica": 0.75,
            "Ideación Paranoide": 0.8,
            "Psicoticismo": 0.9,
            "GSI": 0.85,
            "PST": 0.7,
            "PSDI": 0.9
        }
        
        self.scl90r_data = scl90r_data if scl90r_data else self.default_scl90r_data
        self.a_scale = a_scale
        self.u_scale = u_scale
        self.v_scale = v_scale
        
        # Parámetros del modelo
        self.a = None
        self.u_S = None
        self.v_S = None
        self.u_I = None
        self.v_I = None
        self.u_Sigma = None
        self.v_Sigma = None
        self.fantasy_point = None
        
        # Umbral de angustia
        self.A_cr = np.pi / 4  # Umbral crítico para ruptura
        
        # Calcular parámetros
        self._calculate_parameters()
    
    def _calculate_parameters(self):
        """Calcula todos los parámetros del modelo a partir de los datos del SCL-90-R."""
        # Radio a (escalado por GSI)
        self.a = self.a_scale * self.scl90r_data.get("GSI", 0.85)
        
        # Parámetro u para S (Significante): basado en Ansiedad y Obsesión
        anxiety = self.scl90r_data.get("Ansiedad", 0.95)
        obsession = self.scl90r_data.get("Obsesión-Compulsión", 0.9)
        num_scales = len([k for k in self.scl90r_data.keys() if k not in ["GSI", "PST", "PSDI"]])
        self.u_S = self.u_scale * (anxiety + obsession) / num_scales
        
        # Parámetro v para S: basado en PSDI
        psdi = self.scl90r_data.get("PSDI", 0.9)
        self.v_S = self.v_scale * (1 + psdi)
        
        # Parámetro u para I (Imagen del cuerpo): basado en Somatización y Sensibilidad Interpersonal
        somatization = self.scl90r_data.get("Somatización", 0.8)
        interpersonal = self.scl90r_data.get("Sensibilidad Interpersonal", 0.7)
        self.u_I = self.u_scale * (somatization + interpersonal) / num_scales
        
        # Parámetro v para I: basado en PST
        pst = self.scl90r_data.get("PST", 0.7)
        self.v_I = self.v_scale * (1 + pst)
        
        # Parámetro u para Σ (Síntoma): basado en Psicoticismo y Hostilidad
        psychoticism = self.scl90r_data.get("Psicoticismo", 0.9)
        hostility = self.scl90r_data.get("Hostilidad", 0.6)
        self.u_Sigma = self.u_scale * (psychoticism + hostility) / num_scales
        
        # Parámetro v para Σ: basado en Psicoticismo
        self.v_Sigma = self.v_scale * (1 + psychoticism)
        
        # Punto de fantasía (angustia máxima)
        self.fantasy_point = (np.pi, np.pi / 2)
    
    def horn_torus_surface(self, u_resolution=100, v_resolution=100):
        """
        Genera la superficie paramétrica del horn torus.
        
        Args:
            u_resolution (int): Número de puntos en la dirección u
            v_resolution (int): Número de puntos en la dirección v
            
        Returns:
            tuple: (x, y, z) arrays 2D con las coordenadas de la superficie
        """
        u = np.linspace(0, 2 * np.pi, u_resolution)
        v = np.linspace(0, 2 * np.pi, v_resolution)
        u, v = np.meshgrid(u, v)
        
        # Ecuaciones paramétricas del horn torus (R = r = a)
        x = self.a * (1 + np.cos(v)) * np.cos(u)
        y = self.a * (1 + np.cos(v)) * np.sin(u)
        z = self.a * np.sin(v)
        
        return x, y, z, u, v
    
    def calculate_angustia(self, u, v):
        """
        Calcula la función de angustia A(u, v) como distancia al punto de fantasía.
        
        Args:
            u (array): Array de valores u
            v (array): Array de valores v
            
        Returns:
            array: Valores de angustia A(u, v)
        """
        u_F, v_F = self.fantasy_point
        return np.sqrt((u - u_F)**2 + (v - v_F)**2)
    
    def get_curves(self, u_points=100):
        """
        Genera las curvas S, I, Σ sobre la superficie del horn torus.
        
        Args:
            u_points (int): Número de puntos para cada curva
            
        Returns:
            dict: Diccionario con las coordenadas (x, y, z) de cada curva
        """
        # Generar valores de u para las curvas
        u_vals = np.linspace(0, 2 * np.pi, u_points)
        
        # Curva S (Significante)
        v_vals_S = np.full_like(u_vals, self.v_S)
        x_S = self.a * (1 + np.cos(v_vals_S)) * np.cos(u_vals)
        y_S = self.a * (1 + np.cos(v_vals_S)) * np.sin(u_vals)
        z_S = self.a * np.sin(v_vals_S)
        
        # Curva I (Imagen del cuerpo)
        v_vals_I = np.full_like(u_vals, self.v_I)
        x_I = self.a * (1 + np.cos(v_vals_I)) * np.cos(u_vals)
        y_I = self.a * (1 + np.cos(v_vals_I)) * np.sin(u_vals)
        z_I = self.a * np.sin(v_vals_I)
        
        # Curva Σ (Síntoma)
        v_vals_Sigma = np.full_like(u_vals, self.v_Sigma)
        x_Sigma = self.a * (1 + np.cos(v_vals_Sigma)) * np.cos(u_vals)
        y_Sigma = self.a * (1 + np.cos(v_vals_Sigma)) * np.sin(u_vals)
        z_Sigma = self.a * np.sin(v_vals_Sigma)
        
        return {
            'S': {'x': x_S, 'y': y_S, 'z': z_S, 'color': 'red', 'label': 'S (Significante)'},
            'I': {'x': x_I, 'y': y_I, 'z': z_I, 'color': 'green', 'label': 'I (Imagen del cuerpo)'},
            'Σ': {'x': x_Sigma, 'y': y_Sigma, 'z': z_Sigma, 'color': 'blue', 'label': 'Σ (Síntoma)'}
        }
    
    def get_fantasy_point_3d(self):
        """
        Obtiene las coordenadas 3D del punto de fantasía.
        
        Returns:
            tuple: (x, y, z) coordenadas del punto de fantasía
        """
        u_F, v_F = self.fantasy_point
        x = self.a * (1 + np.cos(v_F)) * np.cos(u_F)
        y = self.a * (1 + np.cos(v_F)) * np.sin(u_F)
        z = self.a * np.sin(v_F)
        return x, y, z
    
    def find_rupture_points(self, u_resolution=50, v_resolution=50):
        """
        Encuentra los puntos donde la angustia supera el umbral crítico (rupturas).
        
        Args:
            u_resolution (int): Número de puntos en u para buscar rupturas
            v_resolution (int): Número de puntos en v para buscar rupturas
            
        Returns:
            tuple: (x_rupture, y_rupture, z_rupture) arrays con coordenadas de rupturas
        """
        u = np.linspace(0, 2 * np.pi, u_resolution)
        v = np.linspace(0, 2 * np.pi, v_resolution)
        u_grid, v_grid = np.meshgrid(u, v)
        
        # Calcular angustia
        A = self.calculate_angustia(u_grid, v_grid)
        
        # Máscara para puntos donde A > A_cr
        rupture_mask = A > self.A_cr
        
        # Coordenadas 3D de los puntos de ruptura
        x = self.a * (1 + np.cos(v_grid)) * np.cos(u_grid)
        y = self.a * (1 + np.cos(v_grid)) * np.sin(u_grid)
        z = self.a * np.sin(v_grid)
        
        return x[rupture_mask], y[rupture_mask], z[rupture_mask], rupture_mask
    
    def plot_3d_model(self, show_ruptures=True, show_curves=True, 
                     save_path=None, dpi=300, interactive=True):
        """
        Visualiza el modelo 3D completo.
        
        Args:
            show_ruptures (bool): Mostrar puntos de ruptura (default: True)
            show_curves (bool): Mostrar curvas S, I, Σ (default: True)
            save_path (str): Ruta para guardar la figura (default: None)
            dpi (int): Resolución para guardar la figura (default: 300)
            interactive (bool): Mostrar figura interactiva (default: True)
            
        Returns:
            fig: Objeto Figure de matplotlib
        """
        # Crear figura
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Generar superficie del horn torus
        x_surf, y_surf, z_surf, u_grid, v_grid = self.horn_torus_surface()
        
        # Calcular angustia para colorear la superficie
        A = self.calculate_angustia(u_grid, v_grid)
        
        # Normalizar angustia para el colormap
        norm = Normalize(vmin=0, vmax=np.max(A))
        cmap = plt.cm.viridis
        
        # Dibujar superficie con color según angustia
        surf = ax.plot_surface(x_surf, y_surf, z_surf, 
                               facecolors=cmap(norm(A)), 
                               alpha=0.6, 
                               rstride=1, cstride=1)
        
        # Añadir colorbar para la angustia
        mappable = ScalarMappable(norm=norm, cmap=cmap)
        mappable.set_array(A)
        cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=20, pad=0.1)
        cbar.set_label('Nivel de Angustia A(u,v)', fontsize=12)
        
        # Dibujar curvas S, I, Σ
        if show_curves:
            curves = self.get_curves()
            for curve_name, curve_data in curves.items():
                ax.plot(curve_data['x'], curve_data['y'], curve_data['z'], 
                        color=curve_data['color'], 
                        linewidth=3, 
                        label=curve_data['label'])
        
        # Dibujar punto de fantasía
        x_F, y_F, z_F = self.get_fantasy_point_3d()
        ax.scatter([x_F], [y_F], [z_F], 
                   color='black', s=200, 
                   label='Fantasía (Punto de Angustia)')
        
        # Dibujar puntos de ruptura
        if show_ruptures:
            x_rupt, y_rupt, z_rupt, _ = self.find_rupture_points()
            if len(x_rupt) > 0:
                ax.scatter(x_rupt, y_rupt, z_rupt, 
                           color='purple', s=50, 
                           label='Rupturas (A > A_cr)')
        
        # Configurar etiquetas y leyenda
        ax.set_xlabel('X (Eje Longitudinal)', fontsize=14, labelpad=10)
        ax.set_ylabel('Y (Eje Transversal)', fontsize=14, labelpad=10)
        ax.set_zlabel('Z (Altura)', fontsize=14, labelpad=10)
        ax.set_title('Modelo 3D del Horn Torus del Icc\n' + 
                     f'Radio a = {self.a:.3f} (GSI = {self.scl90r_data.get("GSI", 0.85)}) | ' + 
                     f'Umbral de Angustia A_cr = {self.A_cr:.3f}', 
                     fontsize=16, pad=20)
        
        # Ajustar proporciones
        max_val = np.max([np.abs(x_surf).max(), np.abs(y_surf).max(), np.abs(z_surf).max()])
        ax.set_xlim([-max_val*1.1, max_val*1.1])
        ax.set_ylim([-max_val*1.1, max_val*1.1])
        ax.set_zlim([-max_val*1.1, max_val*1.1])
        
        # Añadir leyenda
        ax.legend(fontsize=12, loc='upper right')
        
        # Añadir información adicional
        info_text = (
            f"Horn Torus del Icc\n"
            f"a = {self.a:.4f} (R = r = a)\n"
            f"Punto de Fantasía: ({self.fantasy_point[0]:.2f}, {self.fantasy_point[1]:.2f})\n"
            f"Umbral de Ruptura: A_cr = {self.A_cr:.3f}\n\n"
            f"Curvas:\n"
            f"  S (Significante): u={self.u_S:.2f}, v={self.v_S:.2f}\n"
            f"  I (Imagen): u={self.u_I:.2f}, v={self.v_I:.2f}\n"
            f"  Σ (Síntoma): u={self.u_Sigma:.2f}, v={self.v_Sigma:.2f}"
        )
        ax.text2D(0.02, 0.02, info_text, transform=ax.transAxes, 
                  fontsize=10, verticalalignment='bottom', 
                  bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Guardar figura si se especifica
        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
            print(f"Figura guardada en: {save_path}")
        
        # Mostrar figura
        if interactive:
            plt.tight_layout()
            plt.show()
        
        return fig
    
    def plot_deformed_model(self, deformation_factor=0.2, save_path=None):
        """
        Visualiza el modelo con deformaciones en las zonas de ruptura (locura).
        
        Args:
            deformation_factor (float): Factor de deformación (default: 0.2)
            save_path (str): Ruta para guardar la figura (default: None)
            
        Returns:
            fig: Objeto Figure de matplotlib
        """
        # Crear figura
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Generar superficie
        x_surf, y_surf, z_surf, u_grid, v_grid = self.horn_torus_surface()
        
        # Calcular angustia
        A = self.calculate_angustia(u_grid, v_grid)
        rupture_mask = A > self.A_cr
        
        # Aplicar deformación en zonas de ruptura
        z_surf_deformed = z_surf.copy()
        z_surf_deformed[rupture_mask] += deformation_factor * self.a * (A[rupture_mask] - self.A_cr)
        
        # Dibujar superficie deformada
        surf = ax.plot_surface(x_surf, y_surf, z_surf_deformed, 
                               color='orange', 
                               alpha=0.7, 
                               rstride=1, cstride=1,
                               label='Horn Torus Deformado')
        
        # Dibujar curvas (también deformadas donde hay ruptura)
        curves = self.get_curves()
        for curve_name, curve_data in curves.items():
            # Deformar curvas en zonas de ruptura
            u_vals = np.linspace(0, 2 * np.pi, len(curve_data['x']))
            if curve_name == 'S':
                v_vals = np.full_like(u_vals, self.v_S)
            elif curve_name == 'I':
                v_vals = np.full_like(u_vals, self.v_I)
            else:  # Σ
                v_vals = np.full_like(u_vals, self.v_Sigma)
            
            A_curve = self.calculate_angustia(u_vals, v_vals)
            deformation = np.zeros_like(A_curve)
            deformation[A_curve > self.A_cr] = deformation_factor * self.a * (A_curve[A_curve > self.A_cr] - self.A_cr)
            
            z_deformed = curve_data['z'] + deformation
            
            ax.plot(curve_data['x'], curve_data['y'], z_deformed, 
                    color=curve_data['color'], 
                    linewidth=3, 
                    label=f'{curve_data["label"]} (Deformada)')
        
        # Dibujar punto de fantasía
        x_F, y_F, z_F = self.get_fantasy_point_3d()
        ax.scatter([x_F], [y_F], [z_F], 
                   color='black', s=200, 
                   label='Fantasía (Punto de Angustia)')
        
        # Dibujar puntos de ruptura
        x_rupt, y_rupt, z_rupt, _ = self.find_rupture_points()
        if len(x_rupt) > 0:
            # Deformar puntos de ruptura (simplificado para evitar problemas numéricos)
            # Usamos una deformación basada en la distancia desde el origen
            distance_from_origin = np.sqrt(x_rupt**2 + y_rupt**2 + z_rupt**2)
            z_rupt_deformed = z_rupt + deformation_factor * self.a * 0.5
            
            ax.scatter(x_rupt, y_rupt, z_rupt_deformed, 
                       color='purple', s=50, 
                       label='Rupturas (Locura)')
        
        # Configurar etiquetas
        ax.set_xlabel('X (Eje Longitudinal)', fontsize=14, labelpad=10)
        ax.set_ylabel('Y (Eje Transversal)', fontsize=14, labelpad=10)
        ax.set_zlabel('Z (Altura)', fontsize=14, labelpad=10)
        ax.set_title('Modelo 3D del Horn Torus del Icc con Deformación (Locura)\n' + 
                     f'Radio a = {self.a:.3f} | Factor de Deformación = {deformation_factor}', 
                     fontsize=16, pad=20)
        
        # Ajustar proporciones
        max_val = np.max([np.abs(x_surf).max(), np.abs(y_surf).max(), 
                         np.abs(z_surf_deformed).max()])
        ax.set_xlim([-max_val*1.2, max_val*1.2])
        ax.set_ylim([-max_val*1.2, max_val*1.2])
        ax.set_zlim([-max_val*1.2, max_val*1.2])
        
        # Añadir leyenda
        ax.legend(fontsize=12, loc='upper right')
        
        # Guardar figura
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figura deformada guardada en: {save_path}")
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def print_model_summary(self):
        """Imprime un resumen del modelo con todos los parámetros calculados."""
        print("=" * 80)
        print("MODELO 3D DEL HORN TORUS DEL ICC")
        print("=" * 80)
        print("\n--- Datos del SCL-90-R ---")
        for key, value in self.scl90r_data.items():
            print(f"  {key:25s}: {value:.4f}")
        
        print("\n--- Parámetros Geométricos ---")
        print(f"  Radio (a):                    {self.a:.6f}")
        print(f"  Factor de escala (a_scale):   {self.a_scale:.4f}")
        print(f"  Umbral de angustia (A_cr):   {self.A_cr:.6f}")
        
        print("\n--- Curvas S, I, Σ ---")
        print(f"  S (Significante):")
        print(f"    u_S: {self.u_S:.6f}")
        print(f"    v_S: {self.v_S:.6f}")
        print(f"  I (Imagen del cuerpo):")
        print(f"    u_I: {self.u_I:.6f}")
        print(f"    v_I: {self.v_I:.6f}")
        print(f"  Σ (Síntoma):")
        print(f"    u_Σ: {self.u_Sigma:.6f}")
        print(f"    v_Σ: {self.v_Sigma:.6f}")
        
        print("\n--- Punto de Fantasía ---")
        print(f"  (u_F, v_F): ({self.fantasy_point[0]:.6f}, {self.fantasy_point[1]:.6f})")
        x_F, y_F, z_F = self.get_fantasy_point_3d()
        print(f"  Coordenadas 3D: ({x_F:.6f}, {y_F:.6f}, {z_F:.6f})")
        
        print("\n--- Interpretación ---")
        print("  El horn torus representa el Icc como superficie cerrada con autotangencia.")
        print("  Las curvas S, I, Σ están entrelazadas sobre la superficie.")
        print("  El punto de fantasía es el foco de angustia máxima.")
        print("  Cuando A(u,v) > A_cr, se producen rupturas (locura).")
        print("=" * 80)


def main():
    """Función principal para ejecutar el modelo con datos de ejemplo."""
    
    # Datos de ejemplo del SCL-90-R (pueden reemplazarse con datos reales)
    scl90r_data = {
        "Somatización": 0.8,
        "Obsesión-Compulsión": 0.9,
        "Sensibilidad Interpersonal": 0.7,
        "Depresión": 0.85,
        "Ansiedad": 0.95,
        "Hostilidad": 0.6,
        "Ansiedad Fóbica": 0.75,
        "Ideación Paranoide": 0.8,
        "Psicoticismo": 0.9,
        "GSI": 0.85,
        "PST": 0.7,
        "PSDI": 0.9
    }
    
    print("\n" + "=" * 80)
    print("MODELO 3D DEL HORN TORUS DEL ICC CON DATOS DEL SCL-90-R")
    print("=" * 80)
    
    # Crear modelo
    model = HornTorusICCModel(scl90r_data=scl90r_data, a_scale=0.1)
    
    # Imprimir resumen
    model.print_model_summary()
    
    # Visualizar modelo normal
    print("\nGenerando visualización del modelo normal...")
    fig1 = model.plot_3d_model(
        show_ruptures=True,
        show_curves=True,
        save_path='horn_torus_icc_normal.png',
        interactive=False
    )
    
    # Visualizar modelo deformado (locura)
    print("\nGenerando visualización del modelo deformado (locura)...")
    fig2 = model.plot_deformed_model(
        deformation_factor=0.3,
        save_path='horn_torus_icc_deformed.png'
    )
    
    # Mostrar figuras
    plt.show()
    
    print("\n" + "=" * 80)
    print("Visualizaciones generadas:")
    print("  - horn_torus_icc_normal.png: Modelo normal con curvas y rupturas")
    print("  - horn_torus_icc_deformed.png: Modelo deformado (locura)")
    print("=" * 80)


if __name__ == "__main__":
    main()
