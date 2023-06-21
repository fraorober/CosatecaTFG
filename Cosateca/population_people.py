import os
import django
from django.db import connection
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cosateca.settings")

django.setup()

query = f'''
DROP PROCEDURE IF EXISTS populate_users;

CREATE PROCEDURE populate_users()
BEGIN
    DELETE FROM cosatecaapp_productsinlist;
    DELETE FROM cosatecaapp_rating;
    DELETE FROM cosatecaapp_product;
    DELETE FROM auth_user_user_permissions;
	DELETE FROM cosatecaapp_person;
    DELETE FROM auth_user;
    DELETE FROM django_admin_log;
    DELETE FROM cosatecaapp_report;
    DELETE FROM cosatecaapp_verification;
    DELETE FROM cosatecaapp_wishlist;
    DELETE FROM cosatecaapp_messengerservice;

    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('pepe2002', '{make_password('PepitoRodriguez2001')}', 'Pepe', 'Rodríguez López', 'peiptolopezrod@gmail.com', False, False, True, CURRENT_TIMESTAMP());

    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Feria, 16', '41800', '/avatar1.jpg', '678902354', False, (SELECT id FROM auth_user WHERE username = 'pepe2002'));

    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('pedroJose_10', '{make_password('asdf1234')}', 'Pedro José', 'Ramirez Iglesias', 'pedrojose_10@gmail.com', False, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Avenida Carranza, 11', '41809', '/avatar2.jpg', '678987156', False, (SELECT id FROM auth_user WHERE username = 'pedroJose_10'));

    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('admin', '{make_password('admin')}', '', '', 'admin@gmail.com', True, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Feria, 79', '41709', '/avatar3.jpg', '654234156', False, (SELECT id FROM auth_user WHERE username = 'admin'));
   
    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('jesusu', '{make_password('Jesus2001')}', 'Jesus', 'Canales Orta', 'canalesjesus@gmail.com', False, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Marin, 23', '41802', '/avatar3.jpg', '673526712', False, (SELECT id FROM auth_user WHERE username = 'jesusu'));
   
    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('nieves1996', '{make_password('Nieves1996')}', 'Nieves', 'Miranda Díaz', 'nievesmirdiaz@gmail.com', False, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Bodega, 12', '41822', '', '643538234', False, (SELECT id FROM auth_user WHERE username = 'nieves1996'));

    COMMIT;
END;

CALL populate_users();
'''


with connection.cursor() as cursor:
    cursor.execute(query)