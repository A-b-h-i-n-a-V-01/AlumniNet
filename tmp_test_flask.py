from app import create_app, db
from app.models import User
import io

app = create_app()
with app.app_context():
    client = app.test_client()
    
    from flask_login import login_user
    
    with client.application.test_request_context():
        user = User.query.filter_by(email='john.doe@google.com').first()
        
    with client:
        # manually log in
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True
            
        print("Testing GET...")
    res_get = client.get('/upload_photo?category=job_poster')
    
    print("Testing POST...")
    res_post = client.post(
        '/upload_photo', 
        data={
            'photo': (io.BytesIO(b'dummy content'), 'poster.jpg'),
            'event_name': 'My Poster',
            'caption': 'Here is my poster',
            'category': 'job_poster'
        }, 
        follow_redirects=False,
        content_type='multipart/form-data'
    )
    
    print("POST Response Status:", res_post.status_code)
    
    if res_post.status_code == 200:
        html = res_post.data.decode('utf-8')
        if 'is-invalid' in html:
            print("Found validation errors!")
            # Extract errors
            import re
            for m in re.finditer(r'<div class="invalid-feedback">.*?<span>(.*?)</span>.*?</div>', html, re.S):
                print("Error:", m.group(1))
            for m in re.finditer(r'<div class="text-danger small mt-2">.*?</i>(.*?)</div>', html, re.S):
                print("Error (photo):", m.group(1))
            
            # Print form category rendered
            for m in re.finditer(r'<select[^>]*>.*?</select>', html, re.S):
                print("Select rendered as:", m.group(0))

