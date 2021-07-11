db.createUser(
    {
        user: "mongodbusr",
        pwd: "mongodbpwd",
        roles: [
            {
                role: "readWrite",
                db: "somemongodb"
            }
        ] 
    }
)
