import unittest
import os
import re

class TestStylesAndDesignTokens(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.variables_css = os.path.join(self.base_dir, 'static', 'css', 'variables.css')
        self.base_css = os.path.join(self.base_dir, 'static', 'css', 'base.css')
        self.components_css = os.path.join(self.base_dir, 'static', 'css', 'components.css')
        self.theme_js = os.path.join(self.base_dir, 'static', 'js', 'theme.js')
        self.index_html = os.path.join(self.base_dir, 'static', 'index.html')

    def test_css_files_exist(self):
        """Verifica que todos los archivos CSS y JS de estilos existan."""
        self.assertTrue(os.path.exists(self.variables_css), "variables.css debe existir")
        self.assertTrue(os.path.exists(self.base_css), "base.css debe existir")
        self.assertTrue(os.path.exists(self.components_css), "components.css debe existir")
        self.assertTrue(os.path.exists(self.theme_js), "theme.js debe existir")
        self.assertTrue(os.path.exists(self.index_html), "index.html debe existir")

    def test_argentina_palette_tokens_present(self):
        """Verifica que los tokens institucionales de la paleta celeste y blanca argentina y sol de mayo estén definidos."""
        with open(self.variables_css, 'r', encoding='utf-8') as f:
            content = f.read()

        # Debe contener variables primarias (celeste) y acento (sol de mayo / dorado)
        self.assertIn('--color-primary', content)
        self.assertIn('--color-accent', content)
        self.assertIn('--bg-app', content)
        self.assertIn('--bg-surface', content)
        self.assertIn('--text-main', content)

    def test_dark_mode_tokens_present(self):
        """Verifica que existan las reglas para el selector de tema oscuro [data-theme='dark']."""
        with open(self.variables_css, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('[data-theme="dark"]', content)
        self.assertIn('--bg-app:', content)
        self.assertIn('--bg-surface:', content)

    def test_theme_script_logic(self):
        """Verifica que el script theme.js maneje localStorage y cambio de tema."""
        with open(self.theme_js, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('localStorage', content)
        self.assertIn('data-theme', content)
        self.assertIn('prefers-color-scheme', content)

    def test_index_html_loads_styles(self):
        """Verifica que index.html incluya las hojas de estilo y el script del tema."""
        with open(self.index_html, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('variables.css', content)
        self.assertIn('base.css', content)
        self.assertIn('components.css', content)
        self.assertIn('theme.js', content)

if __name__ == '__main__':
    unittest.main()
