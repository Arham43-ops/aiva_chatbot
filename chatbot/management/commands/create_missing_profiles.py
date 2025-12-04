from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chatbot.models import Profile

class Command(BaseCommand):
    help = 'Creates missing user profiles for existing users.'

    def handle(self, *args, **options):
        self.stdout.write('Checking for users without profiles...')
        users_without_profiles = 0
        for user in User.objects.all():
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                users_without_profiles += 1
                self.stdout.write(f'Created profile for user: {user.username}')
        
        if users_without_profiles > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully created {users_without_profiles} missing profile(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('All existing users already have a profile.')) 