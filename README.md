# Insta_clone

#### ERD : 
```mermaid
erDiagram
    User ||--o{ Follow : ""
    User ||--o{ Post : ""
    User ||--o{ PostLike : ""
    User ||--o{ Comment : ""
    User ||--o{ CommentLike : ""
    User }o--|| PostTag : ""
    User {
        userId int PK
        email varchar
        phoneNumber varchar
        name varchar
        username varchar
        password varchar
        profileImage varchar
        profileIntro varchar
        gender varchar
        birth varchar
    }

    Follow {
        userId int FK
        followingId int
        followerId int
    }

    Post ||--o{ Comment : ""
    Post ||--|| PostLike : ""
    Post ||--o{ PostTag : ""
    Post {
        postId int PK
        userId int FK
        imageContent varchar
        textContent varchar
        createdAt datetime
    }

    PostLike {
        postId int FK
        userId int FK
    }
    
    PostTag {
        postId int FK
        userId int FK
        postHashtag varchar
    }
    Comment ||--|| CommentLike : ""
    Comment {
        commentId int PK
        commentText varchar
        createdAt varchar
        postId int FK
        userId int FK
    }

    CommentLike {
        commentId int FK
        userId int FK
    }
```