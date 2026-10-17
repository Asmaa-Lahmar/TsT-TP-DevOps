import unittest

from src.login_service import (
    LoginService,
    MSG_CHAMPS_VIDES,
    MSG_ECHEC,
    MSG_EMAIL_INVALIDE,
    MSG_SUCCES,
    hacher_mot_de_passe,
)


class LoginServiceTest(unittest.TestCase):
    def setUp(self):
        self.hache = hacher_mot_de_passe("Secret123")
        self.service = LoginService({"etudiant@ensa.ma": self.hache})

    def test_identifiants_valides(self):  # CA1
        r = self.service.login("etudiant@ensa.ma", "Secret123")
        self.assertTrue(r.success)
        self.assertEqual(r.message, MSG_SUCCES)

    def test_champs_vides(self):  # CA2
        for email, pwd in [("", "x"), ("etudiant@ensa.ma", ""), (None, None)]:
            r = self.service.login(email, pwd)
            self.assertFalse(r.success)
            self.assertEqual(r.message, MSG_CHAMPS_VIDES)

    def test_format_email_invalide(self):  # CA2
        r = self.service.login("etudiant-ensa.ma", "Secret123")
        self.assertFalse(r.success)
        self.assertEqual(r.message, MSG_EMAIL_INVALIDE)

    def test_message_generique(self):  # CA3
        inconnu = self.service.login("inconnu@ensa.ma", "Secret123")
        mauvais_mdp = self.service.login("etudiant@ensa.ma", "Faux")
        self.assertFalse(inconnu.success)
        self.assertFalse(mauvais_mdp.success)
        self.assertEqual(inconnu.message, mauvais_mdp.message)
        self.assertEqual(inconnu.message, MSG_ECHEC)

    def test_mot_de_passe_jamais_en_clair(self):  # ENF-01
        self.assertNotEqual(self.hache, b"Secret123")
        self.assertTrue(self.hache.startswith(b"$2"))


if __name__ == "__main__":
    unittest.main()
