# koreabaseball-backend

## Requirements
Up to Python 3.12

## Environment Variables
- VERSION
    - description: backend version
    - default: 0.1.0
- DEBUG
    - description: fastapi debug mode - 0 => false, 1 => true
    - default: 0
- SERVER_HOST
    - description: fastapi server host
    - default: 0.0.0.0
- SERVER_PORT
    - description: fastapi server port
    - default: 8000
- POSTGRES_USER
    - description: postgres db user
    - required
- POSTGRES_PASSWORD
    - description: postgres password
    - required
- POSTGRES_HOST
    - description: postgres server host
    - default: localhost
- POSTGRES_PORT
    - description: postgres server port
    - default: 5432
- POSTGRES_DB
    - description: postgres server db name
    - default: kbaseball
- DMOTION_APP_ID
    - description: 4dmotion app id
- DMOTION_API_KEY
    - description: 4dmotion api key
- SECRET_KEY
    - description: JWT SECRET KEY
    - default: 254bcd5390c2749197742e649f77
- REFRESH_SECRET_KEY
    - description: JWT REFRESH SECRET KEY
    - default: be85a59019e1e6ec6be3113
- ARGON2_MEMORY_COST
    - description: Memory cost (in kibibytes)
    - default: 65536
- ARGON2_TIME_COST
    - description: Number of iterations
    - default: 3
- ARGON2_PARALLELISM
    - description: Number of threads
    - default: 4
- ARGON2_SALT_SIZE
    - description: Salt size (in bytes)
    - default: 16