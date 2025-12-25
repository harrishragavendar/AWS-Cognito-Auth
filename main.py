from utils import register_user, verify_user, authenticate_user, access_resource

while True:
    print("==================================================")
    print("||               COGNITO DEMO APP               ||")
    print("==================================================")
    print("|| In this demo, we access a protected endpoint ||")
    print("|| via Amazon Cognito Authentication            ||")
    print("||==============================================||")
    print("||        1. Register new user                  ||")
    print("||        2. Access protected resource          ||")
    print("==================================================")

    choice = int(input("Enter your choice (1/2): "))

    if choice == 1:
        name = input("Enter your name: ")
        email = input("Enter your email Id: ")
        print("""
        Password policy: 
            Minimum length: 8 characters
            At least one uppercase letter (A–Z)
            At least one lowercase letter (a–z)
            At least one number (0–9)
            At least one special character
        """)
        password = input("Enter your password: ")
        registration_status = register_user(email, name, password)

        print("Response from AWS:")
        print(registration_status.json())
        if registration_status.status_code == 200:
            print("Registration successful :) Proceed with email verification")
            verification_code = input("Enter the 6-digit code sent to your email id to verify your account: ")
            verification_status = verify_user(email, verification_code)
            print("Response from AWS:")
            print(verification_status.json())
            if verification_status.status_code == 200:
                print("Verification successful!")
            else:
                print("Verification unsuccessful :( Please try again")
        else:
            print("Registration unsuccessful :( Please try registering again")

    elif choice == 2:
        email = input("Enter your email Id: ")
        password = input("Enter your password: ")
        auth_response = authenticate_user(email, password)
        auth_response_json = auth_response.json()
        print("Response from AWS:")
        print(auth_response_json)
        if auth_response.status_code == 200:
            protected_resource = access_resource(auth_response_json["AuthenticationResult"]["IdToken"])
            if protected_resource.status_code == 200:
                print(protected_resource.json())
            else:
                print("Unable to access protected resource :( Please try again")
        else:
            print("Authentication failed :( Please try again")
