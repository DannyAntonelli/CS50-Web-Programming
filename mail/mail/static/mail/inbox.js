document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function show_emails(email, mailbox) {

  // Create the container of the mail
  const container = document.createElement('div');
  const row = document.createElement('a');
  row.href = "#";
  row.className = "row";

  if (email.read) {
    container.className = "border container read";  
  }
  else {
    container.className = "border container";
  }

  // Heading div
  const heading = document.createElement('a');
  heading.className = "col";
  if (mailbox === "inbox") {
    heading.innerHTML = email.sender;
  }
  else {
    heading.innerHTML = email.recipients[0];
  }
  row.append(heading);

  // Subject div
  const subject = document.createElement('div');
  subject.className = "col-6";
  subject.innerHTML = email.subject;
  row.append(subject);
  
  // Timestamp div
  const timestamp = document.createElement('div');
  timestamp.className = "col";
  timestamp.innerHTML = email.timestamp;
  row.append(timestamp);

  container.append(row);

  // Button to archive and unarchive mail
  if (mailbox !== "sent") {
    const button = document.createElement('button');
    button.className = "btn btn-outline-secondary col";
    
    if (mailbox === "archive") {
      button.innerHTML = "Unarchive";
    }
    else {
      button.innerHTML = "Archive";
    }
    
    row.append(button);  
    button.addEventListener('click', () => archive(email.id, email.archived));
  }
  
  // Add event listeners
  heading.addEventListener('click', () => open_email(email.id));
  subject.addEventListener('click', () => open_email(email.id));
  timestamp.addEventListener('click', () => open_email(email.id));

  // Add the container to the emails view
  document.querySelector('#emails-view').append(container);
}

function open_email(id) {
  
  // Show email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Get the email data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    
    // Mark email as read
    mark_as_read(id);

    // Update the HTML with the data
    document.querySelector('#email-sender').innerHTML = "From: " + email.sender;
    document.querySelector('#email-recipients').innerHTML = "To: " + email.recipients;
    document.querySelector('#email-subject').innerHTML = "Subject: " + email.subject;
    document.querySelector('#email-timestamp').innerHTML = "Date: " + email.timestamp;
    document.querySelector('#email-body').innerHTML = email.body;

    // Add the event listener to the reply button
    document.querySelector('#reply-button').addEventListener('click', () => reply_email(email)); 
  });
}

function reply_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Fill composition field with previous values
  document.querySelector('#compose-recipients').value = email.sender;
  if (!email.subject.startsWith("Re: "))
    email.subject = "Re: " + email.subject;
  document.querySelector('#compose-subject').value = email.subject;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n\n${email.body}\n\n`;
}

function send_email() {
  
  // Create a POST request with the values of the form
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(setTimeout(() => {
    load_mailbox('sent')
  }, 100));
}

function archive(id, current) {

  // Create a PUT request to update the archived value
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: body = JSON.stringify({
      archived: !current
    })
  })
  .then(setTimeout(() => {
    load_mailbox('inbox')
  }, 100));
}

function mark_as_read(id) {

  // Create a PUT request to update the read value
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: body = JSON.stringify({
      read: true
    })
  })
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => show_emails(email, mailbox));
  })
}