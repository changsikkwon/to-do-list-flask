# To_Do_List

📆 2021.01.07 - 2021.01.12

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

### Query Feild
- 유저가 자신의 to do list를 확인하는 qeury
```graphql
query{
  toDoListByUser{
    tag
    content
    targetDate
  }
}
```
- 관리자가 특정 유저의 to do list를 확인하는 qeury
```graphql
query{
  toDoListByMaster(user_id:int!){
    tag
    content
    targetDate
  }
}
```
- 관리자가 유저 list를 확인하는 query(10개씩)
```graphql
query{
  userListByMaster(offset:int!){
    name
    account
  }
}
```

### Mutation Field
- 유저 정보 저장 Mutation
```graphql
mutation{
  createUser(
    account:String!,
    password:String!,
    name:String!,
    isMaster:Boolean=false
  ){
    user{
      account
      password
      name
      isMaster
    }
  }
}
```
- 유저 정보 수정 Mutation
```graphql
mutation{
  createUser(
    account:String,
    password:String,
    name:String,
    isMaster:Boolean
  ){
    user{
      account
      password
      name
      isMaster
    }
  }
}
```
- 유저 정보 인증 Mutation
```graphql
mutation{
  authUser(
  account:String!,
  password:String!
  ){
    accessToken
  }
}
```
- 할 일 정보 저장 Mutation 
```graphql
mutation{
  createToDoList(
  tag:String="ToDo",
  content:String!,
  targetDate:Date
  ){
    toDo{
      tag
      content
      targetDate
    }
  }
}
```
- 할 일 정보 수정 Mutation
```graphql
mutation{
  updateToDoList(
  id:ID!,
  tag:String,
  content:String,
  targetDate:Date,
  isCompleted:Boolean
  ){
    toDo{
      tag
      content
      targetDate
      isCompleted
      completeDate
    }
  }
}
```
- 할 일 정보 삭제 Mutation
```graphql
mutation{
  deleteToDoList(id:ID!){
    deleteToDo
  }
}
```