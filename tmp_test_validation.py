from app import create_app
from app.forms import EventPhotoForm
from werkzeug.datastructures import MultiDict

app = create_app()
with app.app_context():
    from werkzeug.datastructures import FileStorage
    import io
    dummy_file = FileStorage(stream=io.BytesIO(b"my file contents"), filename="test.jpg", content_type="image/jpeg")
    formdata = MultiDict([('category', 'job_poster'), ('event_name', 'My Event'), ('caption', 'My Caption')])
    # We need to pass the file in the files MultiDict
    form = EventPhotoForm(formdata=formdata, meta={'csrf': False}, photo=dummy_file)
    
    print('Initial form data:', form.category.data)
    form.category.choices = [('job_poster', 'Job Poster/Flyer')]
    form.category.data = 'job_poster'
    
    print('Valid:', form.validate())
    print('Errors:', form.errors)
