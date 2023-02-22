from distutils.core import setup, Extension

module = Extension("Remap", sources=["remapmodule.c"])

setup(name="remapping", version="0.01", description="Função map do Processing.", ext_modules=[module])
