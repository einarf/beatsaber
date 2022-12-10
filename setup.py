from setuptools import setup, find_namespace_packages


setup(
    name="beatsaber",
    version="0.2.0",
    description="Beat Saber player",
    url="https://github.com/einarf/beatsaber",
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    packages=find_namespace_packages(include=['beatsaber', 'beatsaber.*']),
    python_requires='>=3.5',
    keywords=['moderngl', 'moderngl-window', 'beat saber'],
    platforms=['any'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        "moderngl-window ~= 2.4.2",
    ],
    entry_points={'console_scripts': [
        'beatsaber = beatsaber.main:run_from_cmd',
    ]},
)
