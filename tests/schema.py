from ariadne import gql

"""
Mutations
"""

create_user = gql(
    """
    mutation create_user($username: String!, $email: String!, $password: String!) {
        create_user(username: $username, email: $email, password: $password)
    }
    """
)

authenticate_user = gql(
    """
    mutation authenticate_user($username: String!, $password: String!) {
        authenticate_user(username: $username, password: $password)
    }
    """
)

request_reset = gql(
    """
    mutation request_reset($email: String!) {
        request_reset(email: $email)
    }
    """
)

password_reset = gql(
    """
    mutation password_reset($email: String!, $new_password: String!) {
        password_reset(email: $email, new_password: $new_password)
    }
    """
)

create_production_record = gql(
    """
    mutation create_production_record($name: String!, $morning_production: String!, $afternoon_production: String!, $evening_production: String!, $production_date: String!) {
        create_production_record(
            name: $name
            morning_production: $morning_production
            afternoon_production: $afternoon_production
            evening_production: $evening_production
            production_date: $production_date
        )
    }
    """
)

update_production_record = gql(
    """
    mutation update_production_record($id: ID!, $name: String!, $morning_production: String!, $afternoon_production: String!, $evening_production: String!, $production_date: String!) {
        update_production_record(
            id: $id
            name: $name
            morning_production: $morning_production
            afternoon_production: $afternoon_production
            evening_production: $evening_production
            production_date: $production_date
        )
    }
    """
)

delete_production_record = gql(
    """
    mutation delete_production_record($id: ID!) {
        delete_production_record(id: $id)
    }
    """
)

create_payment_record = gql(
    """
    mutation create_payment_record($name: String!, $amount: String!, $payment_method: String!, $quantity: String!, $payment_date: String!) {
        create_payment_record(
            name: $name
            amount: $amount
            payment_method: $payment_method
            quantity: $quantity
            payment_date: $payment_date
        )
    }
    """
)

update_payment_record = gql(
    """
    mutation update_payment_record($id: ID!, $name: String!, $amount: String!, $payment_method: String!, $quantity: String!, $payment_date: String!) {
        update_payment_record(
            id: $id
            name: $name
            amount: $amount
            payment_method: $payment_method
            quantity: $quantity
            payment_date: $payment_date
        )
    }
    """
)

delete_payment_record = gql(
    """
    mutation delete_payment_record($id: ID!) {
        delete_payment_record(id: $id)
    }
    """
)

create_customer_record = gql(
    """
    mutation create_customer_record($name: String!, $priority: String!, $phone: String!, $trip: String!, $package: String!) {
        create_customer_record(
            name: $name
            priority: $priority
            phone: $phone
            trip: $trip
            package: $package
        )
    }
    """
)

update_customer_record = gql(
    """
    mutation update_customer_record($id: ID!, $name: String!, $priority: String!, $phone: String!, $trip: String!, $package: String!) {
        update_customer_record(
            id: $id
            name: $name
            priority: $priority
            phone: $phone
            trip: $trip
            package: $package
        )
    }
    """
)

delete_customer_record = gql(
    """
    mutation delete_customer_record($id: ID!) {
        delete_customer_record(id: $id)
    }
    """
)

create_expense_record = gql(
    """
    mutation create_expense_record($item: String!, $category: String!, $amount: String!, $date_of_action: String!) {
        create_expense_record(
            item: $item
            category: $category
            amount: $amount
            date_of_action: $date_of_action
        )
    }
    """
)

update_expense_record = gql(
    """
    mutation update_expense_record($id: ID!, $item: String!, $category: String!, $amount: String!, $date_of_action: String!) {
        update_expense_record(
            id: $id
            item: $item
            category: $category
            amount: $amount
            date_of_action: $date_of_action
        )
    }
    """
)

delete_expense_record = gql(
    """
    mutation delete_expense_record($id: ID!) {
        delete_expense_record(id: $id)
    }
    """
)

delete_auto_reports_record = gql(
    """
    mutation delete_auto_reports_record($id: ID!) {
        delete_auto_reports_record(id: $id)
    }
    """
)

"""
Queries
"""

all_production_records = gql(
    """
    query get_all_production_records {
        get_all_production_records {
            _id
            name
            morning_production
            afternoon_production
            evening_production
            production_date
            created_on
            updated_on
        }
    }
    """
)

all_payment_records = gql(
    """
    query get_all_payment_records {
        get_all_payment_records {
            _id
            name
            amount
            payment_method
            quantity
            payment_date
            created_on
            updated_on
        }
    }
    """
)

all_customer_records = gql(
    """
    query get_all_customer_records {
        get_all_customer_records {
            _id
            name
            priority
            phone
            trip
            package
            created_on
            updated_on
        }
    }
    """
)

all_expense_records = gql(
    """
    query get_all_expense_records {
        get_all_expense_records {
            _id
            item
            category
            amount
            date_of_action
            created_on
            updated_on
        }
    }
    """
)

all_auto_reports_records = gql(
    """
    query get_all_auto_reports_records {
        get_all_auto_reports_records
    }
    """
)

auto_reports_record = gql(
    """
    query get_auto_reports_record($id: ID!) {
        get_auto_reports_record(id: $id)
    }
    """
)
