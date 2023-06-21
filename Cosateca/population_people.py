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
    DELETE FROM cosatecaapp_report;
    DELETE FROM cosatecaapp_rating;
    DELETE FROM cosatecaapp_productsinlist;
    DELETE FROM cosatecaapp_wishlist;
    DELETE FROM cosatecaapp_product;
    DELETE FROM auth_user_user_permissions;
	DELETE FROM cosatecaapp_person;
    DELETE FROM auth_user;
    DELETE FROM django_admin_log;
    DELETE FROM cosatecaapp_verification;
    DELETE FROM cosatecaapp_messengerservice;

    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('pepe2002', '{make_password('PepitoRodriguez2001')}', 'Pepe', 'Rodríguez López', 'peiptolopezrod@gmail.com', False, False, True, CURRENT_TIMESTAMP());

    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Feria, 16', '41800', 'avatar1.jpg', '678902354', False, (SELECT id FROM auth_user WHERE username = 'pepe2002'));

    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('pedroJose_10', '{make_password('asdf1234')}', 'Pedro José', 'Ramirez Iglesias', 'pedrojose_10@gmail.com', False, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Avenida Carranza, 11', '41809', 'avatar2.jpg', '678987156', False, (SELECT id FROM auth_user WHERE username = 'pedroJose_10'));

    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('admin', '{make_password('admin')}', '', '', 'admin@gmail.com', True, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Feria, 79', '41709', '', '654234156', False, (SELECT id FROM auth_user WHERE username = 'admin'));
   
    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('jesusu', '{make_password('Jesus2001')}', 'Jesus', 'Canales Orta', 'canalesjesus@gmail.com', False, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Marin, 23', '41802', 'avatar3.png', '673526712', False, (SELECT id FROM auth_user WHERE username = 'jesusu'));
   
    INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined)
    VALUES ('nieves1996', '{make_password('Nieves1996')}', 'Nieves', 'Miranda Díaz', 'nievesmirdiaz@gmail.com', False, False, True, CURRENT_TIMESTAMP());
    
    INSERT INTO cosatecaapp_person (address, postalCode, imageProfile, phone, banned, user_id)
    VALUES ('Calle Bodega, 12', '41822', '', '643538234', False, (SELECT id FROM auth_user WHERE username = 'nieves1996'));
    
    
    
    
    
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Teléfono móvil', 'productos/movil.png', 'Móvil con muy poco uso. Tiene 4GB de RAM y 128GB de almacenamiento interno. Perefecto para jugar o cualquier función diaria.', 'MOBILE PHONE', CURRENT_TIMESTAMP(), True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'jesusu'));

    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Botas de fútbol', 'productos/botas.jpg', 'Botas de fútbol negras y moradas de tacos. Pensadas para una superficie de césped. No se recomienda su uso para superficies duras.', 'SPORTS', '2023-02-13', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'jesusu'));

    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Balón de fútbol', 'productos/balon.jpg', 'Balón de fútbol de reglamento. Perfecto para cualquier tipo de partido en superficie plana o dura.', 'SPORTS', CURRENT_TIMESTAMP(), True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'jesusu'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Cortacésped', 'productos/cortacesped.jpg', 'Cortacesped a motor. Funciona con gasolina. Muy manejable y eficaz con palanza reguladora para seleccionar la latura del corte.', 'GARDENING', '2023-06-21', False, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pepe2002'));

    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Raqueta de tennis', 'productos/raqueta.jpg', 'Raqueta de tenis de 68x33cm. Mango antideslizante.', 'SPORTS', '2023-06-1', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pepe2002'));

    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Taladro', 'productos/taladro.png', 'Taladro con mucha potencia para hacer cualquier tipo de agujero en la pared. No es inalámbrico pero tiene un cable de gran longitud.', 'TOOLS', '2023-04-16', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pedroJose_10'));

    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Martillo', 'productos/martillo.jpg', 'Martillo con varios tipos de cabezas pensado para golpear varios tipos de tornillos.', 'TOOLS', '2023-05-30', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pedroJose_10'));

    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Cámara DSLR', 'productos/camara.jpg', 'Cámara réflex digital de alta calidad con lentes intercambiables para capturar imágenes profesionales.', 'PHOTOGRAPHY', '2023-04-2', False, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pedroJose_10'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Bicicleta de montaña', 'productos/bicicleta.png', 'Bicicleta todoterreno resistente diseñada para aventuras en terrenos difíciles.', 'SPORTS', '2023-06-19', False, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pedroJose_10'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Sartén antiadherente', 'productos/sarten.jpg', 'Sartén de alta calidad con recubrimiento antiadherente para cocinar sin que los alimentos se peguen.', 'KITCHEN', '2023-05-29', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pedroJose_10'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Mochila impermeable', 'productos/mochila.jpg', 'Mochila espaciosa y resistente al agua, perfecta para llevar tus pertenencias en días lluviosos o en actividades al aire libre.', 'SPORTS', '2023-06-10', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Guitarra acústica', 'productos/guitarra.jpg', 'Guitarra acústica de alta calidad con sonido claro y resonante, ideal para principiantes y músicos experimentados.', 'INSTRUMENTS', '2023-03-15', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));

    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('The Legend of Zelda: Breath of the Wild', 'productos/videojuego.jpg', 'Emocionante juego de aventuras en mundo abierto donde exploras Hyrule y enfrentas desafiantes enemigos.', 'VIDEOGAMES', '2023-06-20', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'jesusu'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('PlayStation 5', 'productos/play.jpeg', 'Consola de videojuegos de última generación con capacidades de juego de alta calidad y características avanzadas.', 'CONSOLES', '2023-06-4', False, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pepe2002'));    
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('El código Da Vinci', 'productos/codigo_da_vinci.jpg', 'Fascinante novela de misterio escrita por Dan Brown, que combina elementos históricos, religiosos y de intriga.', 'BOOKS', '2003-03-18', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('PC Gaming', 'productos/pc.jpg', 'Potente computadora diseñada para gaming con alto rendimiento y capacidad de ejecutar juegos exigentes.', 'PCs', '2023-04-2', True, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'jesusu'));
    
    INSERT INTO cosatecaapp_product(name, image, description, category, publicationDate, availab, userWhoRentProduct_id, userWhoUploadProduct_id)
    VALUES ('Cuadro', 'productos/cuadro.jpg', 'Cuadro muy estético para eventos.', 'ART', '2023-06-18', False, NULL, (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));
    
    
    
    
    
    INSERT INTO cosatecaapp_wishlist(name, owner_id)
    VALUES ('Cosas que quiero', (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));
    
    INSERT INTO cosatecaapp_wishlist(name, owner_id)
    VALUES ('Regalos para mi hermano', (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));
    
    INSERT INTO cosatecaapp_wishlist(name, owner_id)
    VALUES ('Objetos que me hacen falta', (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'jesusu'));
    
    INSERT INTO cosatecaapp_wishlist(name, owner_id)
    VALUES ('Fútbol', (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pedroJose_10'));
    
    
    
    
    
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Balón de fútbol'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Fútbol'));
    
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Botas de fútbol'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Fútbol'));
     
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'The Legend of Zelda: Breath of the Wild'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Regalos para mi hermano'));
    
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Teléfono móvil'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Regalos para mi hermano'));
    
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Teléfono móvil'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Cosas que quiero'));
    
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Cámara DSLR'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Cosas que quiero'));
    
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Cortacésped'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Objetos que me hacen falta'));
    
    INSERT INTO cosatecaapp_productsinlist(product_id, wishList_id)
    VALUES ((SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Sartén antiadherente'), (SELECT cosatecaapp_wishlist.id FROM cosatecaapp_wishlist WHERE name = 'Objetos que me hacen falta'));






    INSERT INTO cosatecaapp_rating(rating, subject, review, create_date, update_date, product_id, user_id)
    VALUES (4, 'Eficaz y preciso', 'Muy útil me ha resultado de gran ayuda y me ha quitado bastante esfuerzo para cortar el jardin', '2023-03-21 20:44:48.000000', '2023-03-21 20:44:48.000000', (SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Cortacésped'), (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));
    
    INSERT INTO cosatecaapp_rating(rating, subject, review, create_date, update_date, product_id, user_id)
    VALUES (3, 'Sin más', '', '2023-05-11 20:44:48.000000', '2023-05-2 20:44:48.000000', (SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'Martillo'), (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));

    INSERT INTO cosatecaapp_rating(rating, subject, review, create_date, update_date, product_id, user_id)
    VALUES (5, 'Genial', 'Me lo he pasado genial con este juego, lo recomiendo', '2023-02-11 20:44:48.000000', '2023-02-11 20:44:48.000000', (SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'The Legend of Zelda: Breath of the Wild'), (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));

    INSERT INTO cosatecaapp_rating(rating, subject, review, create_date, update_date, product_id, user_id)
    VALUES (3, 'No está mal', 'Es un juego chulo, pero la historia se hace demasiado larga.', '2023-03-11 20:44:48.000000', '2023-03-2 20:44:48.000000', (SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'The Legend of Zelda: Breath of the Wild'), (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));

    INSERT INTO cosatecaapp_rating(rating, subject, review, create_date, update_date, product_id, user_id)
    VALUES (1, 'Muy aburrido', 'No me ha gustado nada. Es demasiado largo, se hace eterno y en el mundo abierto tardas mucho en ir de un sitio a otro.', '2023-04-11 20:44:48.000000', '2023-04-2 20:44:48.000000', (SELECT cosatecaapp_product.id FROM cosatecaapp_product WHERE name = 'The Legend of Zelda: Breath of the Wild'), (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));

    
    
    
    
    INSERT INTO cosatecaapp_report(date, observations, reason, capture, reportedUser_id, reportingUser_id)
    VALUES ('2023-06-19', 'Me ha insultado.', 'FRAUDULENT BEHAVIOR', '', (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pepe2002'), (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'nieves1996'));

    INSERT INTO cosatecaapp_report(date, observations, reason, capture, reportedUser_id, reportingUser_id)
    VALUES ('2023-06-19', 'Ha dejado un comentario insultando.', 'FRAUDULENT BEHAVIOR', '', (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'jesusu'), (SELECT cosatecaapp_person.id FROM cosatecaapp_person JOIN auth_user ON cosatecaapp_person.user_id = auth_user.id WHERE username = 'pepe2002')); 
    
    COMMIT;
END;

CALL populate_users();
'''


with connection.cursor() as cursor:
    cursor.execute(query)