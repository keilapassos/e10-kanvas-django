# Entrega 10 - Kanvas

## Projeto: Aplicação (API) em Django semelhante ao Canvas

<br>

### <strong>Atenção</strong>
Esse readme foi feito demonstrando a aplicação completa proposta pela Kenzie Academy Brasil.
Mesmo que a aplicação enviada não contenha todos os endpoints e status codes, em breve ela estará completa.

<br>

## Como instalar e rodar?

para clonar o repositório

```
https://gitlab.com/keila_passos/e10-kanvas
```

Depois que terminar de baixar, é necessário entrar na pasta

```
cd e10-kanvas
```

criar um ambiente virtual e entrar nele:

```
python -m venv venv
```

entrar entrar no ambiente virtual:

```
source venv/bin/activate
```

agora com o ambiente virtual ativado, precisamos instalar as dependências:

```
pip install -r requirements.txt
```

Depois de ter instalado as dependências, é necessário rodar as migrations para que o banco de dados e as tabelas sejam criadas:

```
./manage.py migrate
```

para rodar o projeto:

```
./manage.py runserver
```

o sistema roda em 

```
http://127.0.0.1:8000/
```

## Utilização
Para utilizar este sistema, é necessário utilizar um API Client, como o Insomnia

<br>

## Endpoints (rotas)

### Criação de usuários
Não precisa de autenticação para este endpoint - qualquer pessoa pode criar qualquer usuário.

POST /api/accounts/

  - REQUEST
  ```
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john_doe@bol.com.br",
        "password": "1234",
        "is_admin": false
    }
  ```    
<br>

  - RESPONSE STATUS -> HTTP 201 - CREATED
  ```
    {
        "uuid": "37c65691-d4fc-47e0-aef4-afe7b09c261f",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john_doe@bol.com.br",
        "is_admin": false
    }
  ```

<br>

  1. Caso haja a tentativa de criação de um usuário que já está cadastrado o sistema deverá responder com:

  - RESPONSE STATUS -> HTTP 422 - UNPROCESSABLE ENTITY

  ```     
  {
      "message": "User already exists"
  }  
  ```  

<br>
<hr>
<br>

### Login
A API funcionará com autenticação baseada em token.

POST /api/login/

- REQUEST
  ```
    {
        "email": "john_doe@bol.com.br",
        "password": "1234"
    }
  ```    

- RESPONSE STATUS -> HTTP 200 - OK
  ```
    {
        "token": "76a6683c3a38c40caee04af738d279753e2c4d8d"
    }
  ```

Esse token servirá para identificar o usuário em cada request. Na grande maioria dos endpoints seguintes, será necessário colocar essa informação nos Headers. O header específico para autenticação tem o formato:

```
Authorization: Token <colocar_o_token_aqui>
```

Caso haja a tentativa de login de uma conta que ainda não tenha sido criada, o sistema irá retornar com:

    RESPONSE STATUS -> HTTP 401 - UNAUTHORIZED

<br>
<hr>
<br>

### Listagem de usuários
Esse endpoint servirá para fazermos a listagem de usuários no curso.

GET /api/accounts/
- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

-  RESPONSE STATUS -> HTTP 200 - OK
```    
[
	{
		"uuid": "61039ae4-7016-48d3-b90e-95a78b39e427",
		"first_name": "Maria",
		"last_name": "Joaquina",
		"email": "maria@bol.com.br",
		"is_admin": true
	},
	{
		"uuid": "af8af8b1-7d19-4032-b93d-04c84c66f8e1",
		"first_name": "João",
		"last_name": "Souza",
		"email": "joao@gmail.com.br",
		"is_admin": true
	},
	{
		"uuid": "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd",
		"first_name": "Joaquim",
		"last_name": "Ferreira",
		"email": "joaquim@hotmail.com.br",
		"is_admin": false
	},
	{
		"uuid": "5f2747f3-8899-49d9-b7f9-4ade850db837",
		"first_name": "Marcelo",
		"last_name": "Soares",
		"email": "marcelo@bol.com.br",
		"is_admin": false
	},
	{
		"uuid": "f09c6c88-6cd3-4ed9-b818-432e9f8df11c",
		"first_name": "Pedro",
		"last_name": "Martins",
		"email": "pedro@bol.com.br",
		"is_admin": false
	}
]
```

<br>
<hr>
<br>

### Cadastrando um endereço para o usuário
Esse endpoint deverá fazer a criação do endereço, caso ele não exista e associá-lo ao usuário logado.

PUT /api/address/

- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

  ```
  {
        "zip_code": "123456789",
        "street": "Rua das Flores",
        "house_number": "123",
        "city": "Curitiba",
        "state": "Paraná",
        "country": "Brasil"
  }
  ```

- RESPONSE STATUS -> HTTP 200 - OK
  ```      
    {
        "uuid": "7bf9d19a-2c22-4daa-b7dc-30be78bf1047",
        "street": "Rua das Flores",
        "city": "Curitiba",
        "state": "Paraná",
        "zip_code": "123456789",
        "country": "Brasil",
        "users": [
            {
                "uuid": "38f8b8b7-8edc-4685-9369-643bb85169d2",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john_doe@bol.com.br",
                "is_admin": false
            }
        ]
    }
  ```

<br>
<hr>
<br>

### Criação de cursos
Esse endpoint servirá para realizar a criação de cursos na plataforma Kanvas, somente instrutores poderão criar, atualizar, deletar e matricular estudantes nos cursos.

POST /api/courses/
- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

```
{
    "name": "Django",
    "demo_time": "9:00",
    "link_repo": "https://gitlab.com/turma_django/"
}
```

- RESPONSE STATUS -> HTTP 201 - CREATED

```
{
    "uuid": "7c32c787-83c3-4994-8f45-b6ef113cde5e",
    "name": "Django",
    "demo_time": "09:00:00",
    "created_at": "2022-02-15T19:12:44.914032Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": null,
    "students": []
}
```

<br>
<hr>
<br>

### Listagem de cursos

GET /api/courses/

Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação). A resposta do servidor deve trazer uma lista de cursos, mostrando cada aluno inscrito, no seguinte formato:

- RESPONSE STATUS -> HTTP 200 - OK

```
[
    {
        "uuid": "87556b7e-ac9a-4a8d-9b9f-c2ea7e956a94",
        "name": "Django",
        "demo_time": "09:00:00",
        "created_at": "2022-02-15T19:08:15.927682Z",
        "link_repo": "https://gitlab.com/turma_django/",
        "instructor": null,
        "students": [
            {
                "uuid": "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd",
    "first_name": "Joaquim",
    "last_name": "Ferreira",
    "email": "joaquim@hotmail.com.br",
    "is_admin": false
            }
        ]
    },
    {
        "uuid": "696e31d3-2dd4-42b5-9d2d-4f92035a13fb",
        "name": "Node",
        "demo_time": "09:00:00",
        "created_at": "2022-02-15T19:09:29.898611Z",
        "link_repo": "https://gitlab.com/turma_node/",
        "instructor": null,
        "students": [
            {
                "uuid": "5f2747f3-8899-49d9-b7f9-4ade850db837",
                "first_name": "Marcelo",
                "last_name": "Soares",
                "email": "marcelo@bol.com.br",
                "is_admin": false
            }
        ]
    },
    {
        "uuid": "787673a7-fa4e-4bb8-9ec1-eabbba02fca5",
        "name": "React",
        "demo_time": "09:00:00",
        "created_at": "2022-02-15T19:10:43.883684Z",
        "link_repo": "https://gitlab.com/turma_django/",
        "instructor": {
            "uuid": "61039ae4-7016-48d3-b90e-95a78b39e427",
            "first_name": "Maria",
            "last_name": "Joaquina",
            "email": "maria@bol.com.br",
            "is_admin": true
        },
        "students": [
            {
                "uuid": "5f2747f3-8899-49d9-b7f9-4ade850db837",
                "first_name": "Marcelo",
                "last_name": "Soares",
                "email": "marcelo@bol.com.br",
                "is_admin": false
            },
            {
                "uuid": "f09c6c88-6cd3-4ed9-b818-432e9f8df11c",
                "first_name": "Pedro",
                "last_name": "Martins",
                "email": "pedro@bol.com.br",
                "is_admin": false
            }
        ]
    }
]
```

<br>
<hr>
<br>

### Filtragem de cursos
Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação). A resposta do servidor deve trazer o elemento filtrado pelo course_id informado na url, e deverá ter o seguinte formato.

GET /api/courses/<course_id>/

- RESPONSE STATUS -> HTTP 200 - OK
```
{
    "uuid": "87556b7e-ac9a-4a8d-9b9f-c2ea7e956a94",
    "name": "Django",
    "demo_time": "09:00:00",
    "created_at": "2022-02-15T19:08:15.927682Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": null,
    "students": [
        {
            "uuid": "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd",
            "first_name": "Joaquim",
            "last_name": "Ferreira",
            "email": "joaquim@hotmail.com.br",
            "is_admin": false
        }
    ]
}
```

1 - Caso seja informado um course_id inválido, o sistema deverá responder com:

  - RESPONSE STATUS -> HTTP 404 - NOT FOUND
  ```
  {
      "message": "Course does not exist"
  }
  ```

<br>
<hr>
<br>

### Atualização de cursos
Esse endpoint servirá para fazermos atualizações do curso, fique atento para que, sua aplicação não permita a atualização do nome do curso para outro que já exista.

Deve ser possível fazer atualizações parciais sem a perca de dados.

PATCH /api/courses/<course_id>/

- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

```   
{
    "name": "Node", // Campo opcional
    "demo_time": "8:00", // Campo opcional
    "link_repo": "https://gitlab.com/turma_node/" // Campo opcional
}
```

- RESPONSE STATUS -> HTTP 200 - OK

```  
{
    "uuid": "7c32c787-83c3-4994-8f45-b6ef113cde5e",
    "name": "Node",
    "demo_time": "08:00:00",
    "created_at": "2022-02-15T19:12:44.914032Z",
    "link_repo": "https://gitlab.com/turma_node/",
    "instructor": null,
    "students": []
}
```

1 - Caso tente atualizar um curso que não existe:

- RESPONSE STATUS -> HTTP 404 - NOT FOUND

```                   
{
    "message": "Course does not exist"
}
```

<br>
<hr>
<br>

### Cadastro de instrutor no curso
Esse endpoint será responsável pela inserção de um Instrutor no curso.

Essa rota sempre atualizará o instrutor no curso.

PUT /api/courses/<course_id>/registrations/instructor/

- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

```
{
    "instructor_id": "61039ae4-7016-48d3-b90e-95a78b39e427"
}
```

- RESPONSE STATUS -> HTTP 200

```
{
    "uuid": "87556b7e-ac9a-4a8d-9b9f-c2ea7e956a94",
    "name": "Django",
    "demo_time": "09:00:00",
    "created_at": "2022-02-15T19:08:15.927682Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": {
        "uuid": "61039ae4-7016-48d3-b90e-95a78b39e427",
        "first_name": "Maria",
        "last_name": "Joaquina",
        "email": "maria@bol.com.br",
        "is_admin": true
        },
    "students": [
        {
            "uuid": "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd",
            "first_name": "Joaquim",
            "last_name": "Ferreira",
            "email": "joaquim@hotmail.com.br",
            "is_admin": false
        }
    ]
}
```

Somente usuários do tipo instrutor (ou seja, is_admin == True) podem ser registrados nesse endpoint, caso essa regra seja atendida, ou seja, caso o id pertença a um estudante, a aplicação deverá responder da seguinte maneira:

- RESPONSE STATUS -> HTTP 422 - UNPROCESSABLE ENTITY

```
{
    "message": "Instructor id does not belong to an admin"
}
```

Caso seja informado um course_id inválido, o sistema deverá responder com:

- RESPONSE STATUS -> HTTP 404 - NOT FOUND

```
{
    "message": "Course does not exist"
}
```

Caso seja informado um instructor_id que não pertença a nenhum instrutor, a resposta deve ser:

- RESPONSE STATUS -> HTTP 404 - NOT FOUND
```
{
    "message": "Invalid instructor_id"
}
```

<br>
<hr>
<br>

### Cadastro de estudantes no curso
Esse endpoint será responsável pela matrícula de estudantes no curso.

A lista de estudantes matriculados no curso sempre será atualizada, conforme as informações são enviadas.

PUT /api/courses/<course_id>/registrations/students/

- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

```
{
    "students_id": [
        "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd",
        "5f2747f3-8899-49d9-b7f9-4ade850db837",
        "f09c6c88-6cd3-4ed9-b818-432e9f8df11c"
    ]
}
```

- RESPONSE STATUS -> HTTP 200 - OK

```
{
    "uuid": "87556b7e-ac9a-4a8d-9b9f-c2ea7e956a94",
    "name": "Django",
    "demo_time": "09:00:00",
    "created_at": "2022-02-15T19:08:15.927682Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": {
        "uuid": "61039ae4-7016-48d3-b90e-95a78b39e427",
        "first_name": "Maria",
        "last_name": "Joaquina",
        "email": "maria@bol.com.br",
        "is_admin": true
        },
    "students": [
        {
            "uuid": "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd",
            "first_name": "Joaquim",
            "last_name": "Ferreira",
            "email": "joaquim@hotmail.com.br",
            "is_admin": false
        },
        {
            "uuid": "5f2747f3-8899-49d9-b7f9-4ade850db837",
            "first_name": "Marcelo",
            "last_name": "Soares",
            "email": "marcelo@bol.com.br",
            "is_admin": false
        },
        {
            "uuid": "f09c6c88-6cd3-4ed9-b818-432e9f8df11c",
            "first_name": "Pedro",
            "last_name": "Martins",
            "email": "pedro@bol.com.br",
            "is_admin": false
        }
    ]
}
  
```

Desta forma é possível matricular vários alunos simultaneamente. Da mesma maneira, é possível remover vários estudantes ao mesmo tempo ao registrar novamente a lista de alunos.

- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

```
{
    "students_id": [
        "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd"
    ]
} 
```

- RESPONSE STATUS -> HTTP 200 - OK

```

{
    "uuid": "87556b7e-ac9a-4a8d-9b9f-c2ea7e956a94",
    "name": "Django",
    "demo_time": "09:00:00",
    "created_at": "2022-02-15T19:08:15.927682Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": {
        "uuid": "61039ae4-7016-48d3-b90e-95a78b39e427",
        "first_name": "Maria",
        "last_name": "Joaquina",
        "email": "maria@bol.com.br",
        "is_admin": true
        },
    "students": [
        {
            "uuid": "5fef85a3-61e3-4e03-b6bd-ee544cd9bcdd",
            "first_name": "Joaquim",
            "last_name": "Ferreira",
            "email": "joaquim@hotmail.com.br",
            "is_admin": false
        }
    ]
}
```

Toda requisição feita para esse endpoint deverá atualizar a lista de alunos matriculados no curso. No primeiro exemplo 3 alunos foram vinculados ao curso. No segundo a lista de alunos foi atualizada, matriculando somente um aluno e removendo os outros estudantes que não estavam na nova listagem.

1. Somente usuários do tipo estudante (ou seja, is_admin == False) podem ser matriculados no curso, caso essa regra não seja atendida, ou seja, caso algum id pertença a um instrutor, a aplicação deverá responder com:

- RESPONSE STATUS -> HTTP 422 - UNPROCESSABLE ENTITY

```
{
    "message": "Some student id belongs to an Instructor"
}
```

2. Caso seja informado um course_id inválido, o sistema deverá responder com:

- RESPONSE STATUS -> HTTP 404 - NOT FOUND

```
{
    "message": "Course does not exist"
}
```

<br>
<br>
3. Caso seja informado algum student_id inválido, a resposta deve ser:

- RESPONSE STATUS -> HTTP 404 - NOT FOUND

```
{
    "message": "Invalid students_id list"
}
```

<br>
<hr>
<br>

### Deletar cursos
Este endpoint somente poderá ser acessado por um instrutor e ele realizará a exclusão do curso no sistema.

DELETE /api/courses/<course_id>/

- REQUEST com token:
    - Header -> Authorization: Token < token-do-instrutor >

- RESPONSE STATUS -> HTTP 204 NO CONTENT

<br>
<br>
1. Caso seja informado um course_id inválido, a resposta deve ser:

- RESPONSE STATUS -> HTTP 404 - NOT FOUND

```
{
    "message": "Course does not exist"
}
```

### Tecnologias utilizadas
- Django
- Django Rest Framework
- SQLite
      
      
            
