from setuptools import find_packages, setup

package_name = 'pf1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chris',
    maintainer_email='23589086@sun.ac.za',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "pf_node = pf1.pf:main",
            'syn_pf = pf1.synpf:main',
            'pf_new = pf1.pf_new:main',
        ],
    },
)
