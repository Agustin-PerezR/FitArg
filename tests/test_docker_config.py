import unittest
import os

class TestDockerConfiguration(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dockerfile_path = os.path.join(self.base_dir, 'Dockerfile')
        self.compose_path = os.path.join(self.base_dir, 'docker-compose.yml')
        self.dockerignore_path = os.path.join(self.base_dir, '.dockerignore')

    def test_dockerfile_contents(self):
        """Verifica que el Dockerfile exista y contenga las instrucciones clave."""
        self.assertTrue(os.path.exists(self.dockerfile_path), "Dockerfile debe existir")
        with open(self.dockerfile_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('FROM python:3.12-slim', content)
        self.assertIn('WORKDIR /app', content)
        self.assertIn('EXPOSE 8000', content)
        self.assertIn('HEALTHCHECK', content)
        self.assertIn('CMD ["python", "-m", "app.server"]', content)

    def test_docker_compose_contents(self):
        """Verifica que docker-compose.yml defina el servicio web, puertos y volúmenes."""
        self.assertTrue(os.path.exists(self.compose_path), "docker-compose.yml debe existir")
        with open(self.compose_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('services:', content)
        self.assertIn('fitarg-web:', content)
        self.assertIn('8000:8000', content)
        self.assertIn('fitarg_data:/app/data', content)

    def test_dockerignore_exists(self):
        """Verifica la existencia y contenido de .dockerignore."""
        self.assertTrue(os.path.exists(self.dockerignore_path), ".dockerignore debe existir")
        with open(self.dockerignore_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('__pycache__', content)
        self.assertIn('.git', content)

if __name__ == '__main__':
    unittest.main()
