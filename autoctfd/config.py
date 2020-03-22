"""
A CTFd config.

This class is used to recreate the config files of the CTFd instance

"""

from autoctfd.jsonskeleton import JSON


class Config(JSON):
    def __init__(self, ctf_name, ctf_description, usermode=True):

        self.ctf_version = "2.3.2"
        self.ctf_theme = "core"
        self.ctf_name = ctf_name
        self.ctf_description = ctf_description
        self.user_mode = "users" if usermode else "teams"

        self.start = ""
        self.end = ""
        self.freeze = None

        self.challenge_visibility = "private"
        self.registration_visibility = "public"
        self.score_visibility = "public"
        self.account_visibility = "public"

        self.verify_emails = None
        self.mail_server = None
        self.mail_port = None
        self.mail_tls = None
        self.mail_ssl = None

        self.mail_username = None
        self.mail_password = None
        self.mail_useauth = None

        self.verification_email_subject = "Confirm your account for {ctf_name}"
        self.verification_email_body = "Please click the following link to confirm your email address for {ctf_name}: {url}"

        self.successful_registration_email_subject = (
            "Successfully registered for {ctf_name}"
        )
        self.successful_registration_email_body = (
            "You've successfully registered for {ctf_name}!"
        )
        self.user_creation_email_subject = "Message from {ctf_name}"

        self.user_creation_email_body = "An account has been created for you for {ctf_name} at {url}. \n\nUsername: {name}\nPassword: {password}"

        self.password_reset_subject = "Password Reset Request from {ctf_name}"
        self.password_reset_body = "Did you initiate a password reset? If you didn't initiate this request you can ignore this email. \n\nClick the following link to reset your password:\n{url}"

        self.password_change_alert_subject = (
            "Password Change Confirmation for {ctf_name}"
        )

        self.password_change_alert_body = "Your password for {ctf_name} has been changed.\n\nIf you didn't request a password change you can reset your password here: {url}"

        self.setup = "1"

        self.version_latest = None
