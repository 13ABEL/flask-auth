# think of it as a library
# the library is the resource owner -> all books belong to them
# tokens are library cards
# we (library-goers) are clients
# the library cards allow us to borrow books from the library (resource owner)

# owner of resource creating authorization token
class resourceOwner:
    id = None

    def get_user_id(self):
        return self.id

# 3rd party app w/ token
# defines 3 fields
# -> client_id: identifies client
# -> client_secret: client password
# -> authentication method
class Client:
    client_id = None

    def get_client_id(self):
        return self.client_id

# defines 3 required fields
# -> client_id: id of the client associated with this token
# -> expiry: time at which token will be invalidated
# -> scope: "scope" of access granted for this token
# -> access_token 
# optional fields
# -> refresh token 
class Token:
    client_id = None
    expiry = None
    scope = None

    def get_client_id(self):
        return self.client_id

    def get_expiry(self):
        return self.expiry

    def getScope(self):
        return self.scope