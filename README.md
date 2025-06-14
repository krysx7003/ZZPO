# ZZPO

Baza danych jest dostępna w database/blood\_draws.dp

Jeżeli coś się zepsuje database\_creator.py może postawić bazę od nowa

Po uruchomieniu database\_creator.py BAZA JEST PUSTA.

Generowanie dokumentacji poprzez doxygen

    doxygen Doxyfile 
    
    #Linux
    xdg-open docs/html/index.html

    #Windows 🤮
    start docs/html/index.html

Na razie jest pusto bo do każdej klasy i metody trzeba dodać opis w stylu:

    """A class representing a user.

    Args:
        userID (int): The user's ID (default: -1)
        name (str): The user's first name
        last_name (str): The user's last name
        age (int): The user's age
    """

Baza danych z do <https://dbdiagram.io/>

    Table follows {
      following_user_id integer
      followed_user_id integer
      created_at timestamp
    }

    Table users {
      id integer [primary key]
      username varchar
      role varchar
      created_at timestamp
    }

    Table posts {
      id integer [primary key]
      title varchar
      body text [note: 'Content of the post']
      user_id integer [not null]
      status varchar
      created_at timestamp
    }

    Ref user_posts: posts.user_id > users.id // many-to-one

    Ref: users.id < follows.following_user_id

    Ref: users.id < follows.followed_user_id
