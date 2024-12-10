from django.core.mail import send_mail
from django.utils import timezone
from .models import Task
from datetime import timedelta

def generate_report(subscription):
    current_time = timezone.now()
    if subscription.frequency == 'daily':
        start_date = current_time - timedelta(days=1)
    elif subscription.frequency == 'weekly':
        start_date = current_time - timedelta(weeks=1)
    elif subscription.frequency == 'monthly':
        start_date = current_time - timedelta(weeks=4)
    else:
        return

    tasks = Task.objects.filter(
        due_date__gte=start_date,
        due_date__lte=current_time
    )
    pending_tasks = tasks.filter(status='pending', due_date__lt=current_time)
    pending_tasks.update(status='overdue')

    # Create a visually appealing HTML report
    task_list_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
                color: #333;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }}
            .header {{
                text-align: center;
                background-color: #0078d4;
                color: #fff;
                padding: 15px 0;
                border-radius: 8px 8px 0 0;
            }}
            .task-list {{
                margin: 20px 0;
                padding: 0;
                list-style-type: none;
            }}
            .task {{
                background: #f9f9f9;
                margin-bottom: 10px;
                padding: 10px 15px;
                border-left: 5px solid #0078d4;
                border-radius: 4px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h2>Your Task Report</h2>
            </div>
            <p>Here is your task summary for the selected period:</p>
            <ul class="task-list">
    """

    for task in tasks:
        task_list_html += f"""
            <li class="task">
                <strong>Title:</strong> {task.title}<br>
                <strong>Status:</strong> {task.status}<br>
                <strong>Description:</strong> {task.description}<br>
                <strong>Due Date:</strong> {task.due_date.strftime('%Y-%m-%d %H:%M:%S')}
            </li>
        """

    task_list_html += """
            </ul>
            <div class="footer">
                <p>Thank you for using our task management system.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Send email to the user
    send_mail(
        'Your Periodic Task Report',
        '',
        'hamdihossam461@gmail.com',
        [subscription.user.email],
        html_message=task_list_html,
    )

