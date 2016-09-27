from django.shortcuts import render
from forms import ContactForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'personal/home.html')

def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the 
            # contact information
            template = get_template('personal/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "You got a new message from " + contact_name + ' ' + contact_email,
                content,
                contact_email,
                ['justaskumelis@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'personal/contact.html', {
        'form': form_class,
    })