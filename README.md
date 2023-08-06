# backend_FASTAPI
tested: ![Tested](https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)  ![Tested](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)  ![Tested](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)  
  
![](https://img.shields.io/badge/python-3.8-blue) ![](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)   


### Backend Installation  
Manual with docker:  

```shell
docker network create healthwatch  
docker build -t <server Name> .
docker-compose up -d
```

Auto with docker:  

```shell
docker pull lavi02/healthwatch-server
```

Manual with virtualenv:  

```shell
git clone git@github.com:ACT-HealthWatch/backend_FASTAPI.git  
python3 -m venv <project name>  
rsync -av --exclude 'venv/__pycache__/' \  
            --exclude 'backend_FASTAPI/bin/' \  
            --exclude 'backend_FASTAPI/include/' \  
            --exclude 'backend_FASTAPI/lib/' \  
            --exclude 'backend_FASTAPI/pyvenv.cfg' \  
            backend_FASTAPI <project name>  
cd <project name>  
pip3 install -r requirements.txt  
uvicorn app:app --reload
```