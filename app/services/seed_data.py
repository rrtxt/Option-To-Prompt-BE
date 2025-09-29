from sqlmodel import Session, select
from app.models import Platform, Action, Variable, Template, VariableType
from app.database import engine


def seed_database():
    """Seed database with initial data from frontend mock data"""
    
    with Session(engine) as session:
        # Check if data already exists
        existing_platforms = session.exec(select(Platform)).first()
        if existing_platforms:
            print("Database already seeded, skipping...")
            return
        
        print("Seeding database with initial data...")
        
        # Create platforms
        platforms_data = [
            {"name": "Instagram", "slug": "instagram", "description": "Instagram social media platform"},
            {"name": "Facebook", "slug": "facebook", "description": "Facebook social media platform"},
            {"name": "LinkedIn", "slug": "linkedin", "description": "LinkedIn professional network"},
            {"name": "Twitter/X", "slug": "twitter", "description": "Twitter/X social media platform"},
            {"name": "YouTube", "slug": "youtube", "description": "YouTube video platform"},
            {"name": "TikTok", "slug": "tiktok", "description": "TikTok short video platform"},
            {"name": "Email", "slug": "email", "description": "Email communication"},
            {"name": "WhatsApp", "slug": "whatsapp", "description": "WhatsApp messaging platform"},
        ]
        
        platforms = {}
        for platform_data in platforms_data:
            platform = Platform(**platform_data)
            session.add(platform)
            session.commit()
            session.refresh(platform)
            platforms[platform.slug] = platform
        
        # Create actions and their variables/templates
        actions_data = {
            "instagram": [
                {
                    "name": "Create Post", "slug": "post", 
                    "description": "Create a new Instagram post",
                    "variables": [
                        {"name": "content", "label": "Post Content", "type": VariableType.TEXTAREA, "required": True, "placeholder": "What do you want to post?", "order": 1},
                        {"name": "image_path", "label": "Image Path (optional)", "type": VariableType.TEXT, "required": False, "placeholder": "/path/to/image.jpg", "order": 2},
                        {"name": "hashtags", "label": "Hashtags", "type": VariableType.TEXT, "required": False, "placeholder": "#example #hashtag", "order": 3}
                    ],
                    "template": """You are a web automation agent tasked with creating an Instagram post. Follow these steps carefully:

1. Navigate to Instagram.com if not already there
2. Locate the 'Create' or '+' button to start a new post
3. {% if image_path %}Upload the image from: {{ image_path }}
4. {% endif %}Add the following content to the caption field: "{{ content }}"
5. {% if hashtags %}Include these hashtags in the post: {{ hashtags }}
6. {% endif %}Review the post preview to ensure accuracy
7. Click 'Share' or 'Post' to publish

If any step fails, try alternative approaches:
- Look for similar elements with different text/labels
- Check if Instagram's interface has changed
- Provide clear error messages if elements cannot be found

Expected outcome: A new Instagram post published with the specified content{% if image_path %} and image{% endif %}{% if hashtags %} and hashtags{% endif %}."""
                },
                {
                    "name": "Create Story", "slug": "story",
                    "description": "Create an Instagram story",
                    "variables": [
                        {"name": "content", "label": "Story Content", "type": VariableType.TEXTAREA, "required": True, "placeholder": "Story text or description", "order": 1},
                        {"name": "media_path", "label": "Media Path", "type": VariableType.TEXT, "required": True, "placeholder": "/path/to/media.jpg", "order": 2},
                        {"name": "duration", "label": "Duration (seconds)", "type": VariableType.NUMBER, "required": False, "placeholder": "15", "order": 3}
                    ],
                    "template": """You are a web automation agent tasked with creating an Instagram story. Execute these steps:

1. Navigate to Instagram.com if not already there
2. Look for the 'Your story' or camera icon to create a new story
3. Upload or select media from: {{ media_path }}
4. Add the following text/content to the story: "{{ content }}"
5. {% if duration %}Set story duration to {{ duration }} seconds if the option is available
6. {% endif %}Preview the story to ensure it looks correct
7. Click 'Share to your story' or 'Publish' to post

Fallback strategies if elements are not found:
- Try clicking the profile picture or '+' icon
- Look for 'Add to story' options
- Check mobile vs desktop interface differences
- Report specific errors encountered

Expected outcome: A new Instagram story published with the specified content and media{% if duration %} with {{ duration }} second duration{% endif %}."""
                },
                {
                    "name": "Send Direct Message", "slug": "send_dm",
                    "description": "Send a direct message",
                    "variables": [
                        {"name": "recipient", "label": "Recipient Username", "type": VariableType.TEXT, "required": True, "placeholder": "@username", "order": 1},
                        {"name": "message", "label": "Message", "type": VariableType.TEXTAREA, "required": True, "placeholder": "Your message here...", "order": 2}
                    ],
                    "template": """You are a web automation agent tasked with sending an Instagram direct message. Follow these steps:

1. Navigate to Instagram.com if not already there
2. Look for the 'Messages' icon or 'Direct' button (usually paper plane icon)
3. Click 'New message' or '+' to start a new conversation
4. Search for and select the recipient: {{ recipient }}
5. Type the following message in the text field: "{{ message }}"
6. Click 'Send' to deliver the message

Error handling and alternatives:
- If recipient not found, verify the username is correct
- Try searching without '@' symbol if included
- Check if the account allows messages from non-followers
- Look for message requests or restricted messaging notifications

Expected outcome: A direct message sent to {{ recipient }} with the content: "{{ message }}"."""
                }
            ],
            "facebook": [
                {
                    "name": "Create Post", "slug": "post",
                    "description": "Create a Facebook post",
                    "variables": [
                        {"name": "content", "label": "Post Content", "type": VariableType.TEXTAREA, "required": True, "placeholder": "What's on your mind?", "order": 1},
                        {"name": "privacy", "label": "Privacy Setting", "type": VariableType.SELECT, "required": True, "options": ["public", "friends", "only_me"], "order": 2},
                        {"name": "image_path", "label": "Image Path (optional)", "type": VariableType.TEXT, "required": False, "placeholder": "/path/to/image.jpg", "order": 3}
                    ],
                    "template": """You are a web automation agent tasked with creating a Facebook post. Execute these steps:

1. Navigate to Facebook.com if not already there
2. Locate the status update box (usually says "What's on your mind?" or similar)
3. Click in the text area to activate it
4. Type the following content: "{{ content }}"
5. {% if image_path %}Click 'Photo/Video' or camera icon and upload image from: {{ image_path }}
6. {% endif %}Set privacy to {{ privacy }} by clicking the privacy selector (audience icon)
7. Review the post content and settings
8. Click 'Post' or 'Share' to publish

Privacy setting guidance:
- "public": Look for globe icon or "Public" option
- "friends": Look for friends icon or "Friends" option  
- "only_me": Look for lock icon or "Only me" option

Error handling:
- If privacy option not found, document available options
- Try alternative upload methods if image upload fails
- Check for content policy warnings or restrictions

Expected outcome: A Facebook post published with content "{{ content }}"{% if image_path %} and image from {{ image_path }}{% endif %} with {{ privacy }} privacy setting."""
                }
            ],
            "email": [
                {
                    "name": "Send Email", "slug": "send_email",
                    "description": "Send an email message",
                    "variables": [
                        {"name": "recipient", "label": "Recipient Email", "type": VariableType.EMAIL, "required": True, "placeholder": "recipient@example.com", "order": 1},
                        {"name": "subject", "label": "Subject", "type": VariableType.TEXT, "required": True, "placeholder": "Email subject", "order": 2},
                        {"name": "body", "label": "Email Body", "type": VariableType.TEXTAREA, "required": True, "placeholder": "Your email content...", "order": 3},
                        {"name": "cc", "label": "CC (optional)", "type": VariableType.TEXT, "required": False, "placeholder": "cc@example.com", "order": 4}
                    ],
                    "template": """You are a web automation agent tasked with sending an email. Follow these steps:

1. Navigate to the email service (Gmail, Outlook, etc.) if not already there
2. Look for 'Compose', 'New', or '+' button to create a new email
3. Fill in the recipient field with: {{ recipient }}
4. {% if cc %}Add {{ cc }} to the CC field
5. {% endif %}Enter the subject: "{{ subject }}"
6. Type the email body: "{{ body }}"
7. Review all fields for accuracy
8. Click 'Send' to deliver the email

Platform-specific guidance:
- Gmail: Look for red 'Compose' button
- Outlook: Look for 'New message' or 'New mail'
- Yahoo: Look for 'Compose' or 'Write'

Error handling:
- Verify email addresses are valid format
- Check for auto-complete suggestions if recipient not found
- Handle security prompts or two-factor authentication
- Report any delivery failure notifications

Expected outcome: Email sent to {{ recipient }} with subject "{{ subject }}"{% if cc %} and CC to {{ cc }}{% endif %}."""
                }
            ]
        }
        
        # Create actions, variables, and templates
        for platform_slug, platform_actions in actions_data.items():
            platform = platforms[platform_slug]
            
            for action_data in platform_actions:
                # Create action
                action = Action(
                    name=action_data["name"],
                    slug=action_data["slug"],
                    description=action_data["description"],
                    platform_id=platform.id
                )
                session.add(action)
                session.commit()
                session.refresh(action)
                
                # Create variables
                for var_data in action_data["variables"]:
                    variable = Variable(
                        name=var_data["name"],
                        label=var_data["label"],
                        type=var_data["type"],
                        required=var_data["required"],
                        placeholder=var_data.get("placeholder"),
                        order=var_data["order"],
                        action_id=action.id,
                        options=var_data.get("options")
                    )
                    session.add(variable)
                
                # Create template
                template = Template(
                    content=action_data["template"],
                    action_id=action.id
                )
                session.add(template)
        
        session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
