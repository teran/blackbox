"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test import TestCase

from transmission.models import Torrent, File, Hardlink, View


class BlackboxUnitTest(TestCase):
    def test_create_torrent(self):
        torrent = Torrent(
            hash='123',
            name='test_torrent'
        )
        torrent.save()

        torrent = Torrent.objects.get(hash='123')

        self.assertEqual(torrent.hash, '123')
        self.assertEqual(torrent.name, 'test_torrent')

    def test_create_file(self):
        torrent = Torrent(
            hash='123',
            name='test_torrent'
        )
        torrent.save()

        file = File(
            filename='test_filename.name',
            torrent=torrent
        )
        file.save()

        file = File.objects.get(
            filename='test_filename.name',
            torrent=torrent
        )

        self.assertEqual(file.filename, 'test_filename.name')
        self.assertEqual(file.torrent.id, torrent.id)

    def test_create_hardlink(self):
        torrent = Torrent(
            hash='123',
            name='test_torrent'
        )
        torrent.save()

        file = File(
            filename='test_filename.name',
            torrent=torrent
        )
        file.save()

        user = User(username='test_user')
        user.save()

        hardlink = Hardlink(
            token='123456',
            file=file,
            user=user
        )
        hardlink.save()

        self.assertEqual(hardlink.token, '123456')
        self.assertEqual(hardlink.file, file)
        self.assertEqual(hardlink.user, user)

    def test_create_view(self):
        torrent = Torrent(
            hash='123',
            name='test_torrent'
        )
        torrent.save()

        file = File(
            filename='test_filename.name',
            torrent=torrent
        )
        file.save()

        user = User(username='test_user')
        user.save()

        view = View(
            file=file,
            user=user
        )
        view.save()

        view = View.objects.get(
            file=file,
            user=user
        )

        self.assertEqual(view.file, file)
        self.assertEqual(view.user, user)


class BlackboxCITest(TestCase):
    def test_dummy(self):
        pass
