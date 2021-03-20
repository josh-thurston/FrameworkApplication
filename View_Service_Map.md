# Framework Applicaiton View and Service Tree

Checklist
[ x ] - Account views
[ x ] - Assessment views
[ x ] - Dashboard views
[ x ] - Framework views
[ x ] - Home views
[ x ] - Product views
[ x ] -  User admin views
[ x ] - Vendors views


## Registration
views
- account_views.py
    - services
        - user_services.create_user()
            - tenant_service.find_tenant()
        - tenant_services.create_tenant (account_services.py)
            - user_services.set_admin()
            - user_services.administrator_of()

## Login
views
- account_views.py
    - services
        - user_services.login_user()
            - user_services.verify_hash()
            - user_services.update_previous_logon()
            - TODO: Need to finish check status function
        - user_services.check_status()

## User Profile
views
- account_views
    - services
        - user_service.get_profile()
        - user_service.get_company_info()
        - user_service.check_user_role()
        - user_service.update_title()
        - tenant_service.update_industry()
        - tenant_service.update_city()
        - tenant_service.update_country()
        - tenant_service.update_postal()
        - tenant_service.update_state()
        - tenant_service.update_website()

## User Admin 
views
- user_admin_views
    - user_service.get_user_info(encoded)
    - user_services.check_user_role()
    - user_service.get_profile()
    - tenant_services.get_company_info()
    - user_service.get_company_name()
    - user_service.get_users()
    - user_services.update_role()
        - user_services.drop_user_to_tenant()
        - user_services.update_user_to_tenant()
    - user_service.update_status()
    - user_services.update_permission()
    - user_service.decline_access()
        - user_services.drop_user_to_tenant()
        - user_services.delete_user()




hashed_password:
$6$rounds=171204$DEqXaI2r.4sNnfR0$MM5NPhn5NkOAmLG9MOwZuQ9AdqGkiYtT8v4CzBOh262EoohDV57BLzW7OEBXZNojFuC5cRCTKL9zAbW2QnjEt.
hashed_password:
$6$rounds=171204$DEqXaI2r.4sNnfR0$MM5NPhn5NkOAmLG9MOwZuQ9AdqGkiYtT8v4CzBOh262EoohDV57BLzW7OEBXZNojFuC5cRCTKL9zAbW2QnjEt.