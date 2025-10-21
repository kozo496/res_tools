from setuptools import setup, find_packages

setup(
    name="res",                     # パッケージ名
    version="0.0.1",                  # バージョン
    packages=find_packages(where="src"),  # src配下を探索
    package_dir={"": "src"},          # ルートは src にある
    python_requires=">=3.11",          # 対応Pythonバージョン
    install_requires=[
        "flowkit==1.2.3",
        "fcsparser==0.2.8",
        "numpy<2",
        "pandas>=1.5.3",
    ],
)
