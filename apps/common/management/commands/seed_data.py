import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.users.models import Profile, Role
from apps.properties.models import Property, Room
from apps.bookings.models import Booking
from apps.payments.models import Payment
from apps.tasks.models import Task
from apps.reviews.models import Review

User = get_user_model()

class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de ejemplo para desarrollo.'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando seed de datos...')

        # 1. Crear usuarios
        admin = self.create_user('admin@example.com', 'admin123', 'Admin', 'Principal', Role.ADMIN, is_staff=True, is_superuser=True)
        owner = self.create_user('owner@example.com', 'owner123', 'Carlos', 'Pérez', Role.OWNER)
        staff1 = self.create_user('staff1@example.com', 'staff123', 'Luis', 'García', Role.STAFF)
        staff2 = self.create_user('staff2@example.com', 'staff123', 'Ana', 'Martínez', Role.STAFF)
        guest1 = self.create_user('guest1@example.com', 'guest123', 'John', 'Doe', Role.GUEST)
        guest2 = self.create_user('guest2@example.com', 'guest123', 'María', 'López', Role.GUEST)

        # 2. Crear propiedades
        prop1 = Property.objects.create(
            name='Casa Colonial Centro',
            description='Hermosa casa colonial en el corazón de La Habana Vieja.',
            address='Calle Obispo 123',
            city='La Habana',
            province='La Habana',
            price_per_night=Decimal('60.00'),
            max_guests=6,
            services=['wifi', 'aire acondicionado', 'cocina'],
            owner=owner,
            is_active=True
        )
        prop2 = Property.objects.create(
            name='Apartamento Vedado',
            description='Apartamento moderno cerca del Malecón.',
            address='Calle Línea 456',
            city='La Habana',
            province='La Habana',
            price_per_night=Decimal('45.00'),
            max_guests=4,
            services=['wifi', 'lavadora'],
            owner=owner,
            is_active=True
        )

        # 3. Habitaciones
        room1 = Room.objects.create(
            property=prop1,
            room_number='101',
            room_type='double',
            capacity=2,
            price_per_night=Decimal('30.00'),
            amenities=['aire acondicionado', 'baño privado'],
            is_available=True
        )
        room2 = Room.objects.create(
            property=prop1,
            room_number='102',
            room_type='triple',
            capacity=3,
            price_per_night=Decimal('40.00'),
            amenities=['balcón', 'vista a la calle'],
            is_available=True
        )
        room3 = Room.objects.create(
            property=prop2,
            room_number='201',
            room_type='suite',
            capacity=4,
            price_per_night=Decimal('50.00'),
            amenities=['jacuzzi', 'cocina'],
            is_available=True
        )

        # 4. Reservas
        booking1 = Booking.objects.create(
            guest=guest1,
            property=prop1,
            room=room1,
            check_in=date.today() + timedelta(days=10),
            check_out=date.today() + timedelta(days=15),
            number_of_guests=2,
            total_price=Decimal('150.00'),
            status=Booking.BookingStatus.CONFIRMED,
            notes='Llegada por la tarde'
        )
        booking2 = Booking.objects.create(
            guest=guest2,
            property=prop2,
            room=room3,
            check_in=date.today() + timedelta(days=20),
            check_out=date.today() + timedelta(days=25),
            number_of_guests=3,
            total_price=Decimal('250.00'),
            status=Booking.BookingStatus.PENDING
        )

        # 5. Pagos
        Payment.objects.create(
            booking=booking1,
            amount=Decimal('75.00'),
            method=Payment.PaymentMethod.CASH,
            reference='Pago inicial'
        )
        Payment.objects.create(
            booking=booking1,
            amount=Decimal('75.00'),
            method=Payment.PaymentMethod.BANK_TRANSFER,
            reference='Transferencia #123'
        )

        # 6. Tareas
        Task.objects.create(
            title='Limpieza habitación 101',
            description='Limpiar antes de la llegada del huésped.',
            task_type=Task.TaskType.CLEANING,
            status=Task.TaskStatus.PENDING,
            assigned_to=staff1,
            booking=booking1,
            room=room1,
            due_date=date.today() + timedelta(days=9)
        )
        Task.objects.create(
            title='Preparar suite para check-in',
            task_type=Task.TaskType.CHECKIN_PREP,
            status=Task.TaskStatus.IN_PROGRESS,
            assigned_to=staff2,
            booking=booking2,
            room=room3,
            due_date=date.today() + timedelta(days=19)
        )

        # 7. Opiniones
        Review.objects.create(
            booking=booking1,
            property=prop1,
            rating=5,
            comment='Excelente ubicación, muy limpio.'
        )
        Review.objects.create(
            booking=booking2,
            property=prop2,
            rating=4,
            comment='Buen apartamento, un poco ruidoso.'
        )

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo creados exitosamente.'))

    def create_user(self, email, password, first_name, last_name, role, is_staff=False, is_superuser=False):
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        Profile.objects.create(user=user)
        return user