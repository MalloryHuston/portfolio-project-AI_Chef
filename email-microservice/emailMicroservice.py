import pika, sys, os
from tkinter import *
from tkinter import messagebox
import smtplib
from email.message import EmailMessage


def communication():
    """
    A function that will constantly run and wait for a message from RabbitMQ communication
    line. Once message is received, will open up the email GUI.
    """
    openEmail = ""

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email')

    def callback(ch, method, properties, body):
        openEmail = body
        if str(body) == "b'yes'":
            email()

        print(" [x] Received %r" % body)

    channel.basic_consume(queue='email', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        communication()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


def email():
    """
    Email GUI. Will open when message is received.
    Users must put in message content and subject content for message
    to be sent.
    """
    root = Tk()
    root.title("Email")
    root.geometry("900x450")

    frame = Frame(root, height=200, width=900)
    frame.pack()

    def display_text():
        """
        Populates the email message with the contents from the widgets.
        Message must contain body content and subject content.
        !!!IMPORTANT!!! s.login can be changed to any email but
        the password must be the app password for gmail. Not regular
        gmail password. The second argument in s.sendmail is the email
        you want the message to go to.
        """

        bodyString = emailBody.get(1.0, END)
        if len(bodyString) == 1:
            messagebox.showerror("Show Error", "No Message Inputted")

        elif len(subjectMessage.get()) == 0:
            messagebox.showerror("Show Error", "No Subject Inputted")

        else:
            msg = EmailMessage()
            msg.set_content(bodyString)
            msg['Subject'] = subjectMessage.get()
            msg['From'] = "hustonm@oregonstate.edu"
            msg['To'] = "mallorylhuston@gmail.com"

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            # login for smtplib server (password is gmail app password SEE INFO =
            # https://support.google.com/accounts/answer/185833?hl=en)
            s.login('CS361SoftwareEngineering@gmail.com', 'yoevauamcinrcxvs')
            # First argument is where the email is getting sent from. Second argument is where it is going
            s.sendmail('CS361SoftwareEngineering', 'mallorylhuston@gmail.com', msg.as_string())
            s.quit()
            emailBody.delete(1.0, END)
            subjectMessage.delete(0, END)
            messagebox.showinfo("Success", "Email Successfully Sent")
            return

    # Widgets added for email subject and email body
    emailSubject = Label(frame, text="Subject")
    emailSubject.pack()

    bodyTitle = Label(root, text="Message")
    bodyTitle.pack()

    subjectMessage = Entry(frame, width=50)
    subjectMessage.focus_set()
    subjectMessage.pack()

    emailBody = Text(root, width=60, height=20, bg="lightgray")
    emailBody.pack()

    button_frame = Frame(root)
    button_frame.pack()

    # will call display text to send email
    submitButton = Button(
        root,
        text="Send Email",
        command=display_text,
        fg="black")

    submitButton.pack(side=BOTTOM)

    root.mainloop()


while True:
    communication()
