# To_Do_List

### 사용한 기술
- Flask
- Mysql
- Graphql
- Sqlalchemy

### 구조
- models.py : DB연결과 각 테이블 Column의 type을 지정하는 파일입니다.
- query.py : Graphql Query 타입에 해당하는 모든 로직을 처리하는 파일입니다.
- mutation.py : Graphql Mutation 타입에 해당하는 모든 로직을 처리하는 파일입니다.
- app.py : 서버 가동을 위해 필요한 정보를 담고 있는 파일입니다.
- run.py : app.py를 기반으로 서버 가동만을 위한 파일입니다.
