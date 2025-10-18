from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Users (super heroes)
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "Marvel"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain Marvel", "email": "captainmarvel@marvel.com", "team": "Marvel"},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Teams
        teams = [
            {"name": "Marvel", "members": ["Spider-Man", "Iron Man", "Captain Marvel"]},
            {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user": "Superman", "activity": "Flying", "duration": 120},
            {"user": "Batman", "activity": "Martial Arts", "duration": 90},
            {"user": "Spider-Man", "activity": "Web Swinging", "duration": 60},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "Marvel", "points": 300},
            {"team": "DC", "points": 250},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"name": "Strength Training", "suggested_for": ["Superman", "Iron Man"]},
            {"name": "Agility Drills", "suggested_for": ["Spider-Man", "Batman"]},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
