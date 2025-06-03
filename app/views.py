# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from django.db.models import Q
# from django.contrib import messages
# from django.views.decorators.http import require_POST
# from .models import Drug, Sale, SaleItem, PaymentMethod, OTPVerification
# from .forms import DrugForm, SaleForm, SaleItemForm

# from django.shortcuts import render
# from django.db.models import Sum, Count
# from django.db.models.functions import TruncDate
# from .models import Sale
# from .utils import send_sms


# # def request_otp(request):
# #     if request.method == 'POST':
# #         phone = request.POST.get('phone_number')
# #         otp_entry = OTPVerification.objects.create(phone_number=phone)
# #         send_sms(phone, f"Your OTP is {otp_entry.otp_code}")
# #         print(f"OTP sent to {phone}: {otp_entry.otp_code}")  # For debugging, remove in production
# #         request.session['otp_id'] = otp_entry.id
# #         return redirect('verify_otp')
# #     return render(request, 'app/request_otp.html')

# # def verify_otp(request):
# #     if request.method == 'POST':
# #         otp = request.POST.get('otp')
# #         otp_id = request.session.get('otp_id')
# #         otp_record = OTPVerification.objects.get(id=otp_id)

# #         if otp_record.otp_code == otp and not otp_record.is_verified:
# #             otp_record.is_verified = True
# #             otp_record.save()
# #             request.session['authenticated'] = True
# #             return redirect('home')
# #         else:
# #             messages.error(request, 'Invalid OTP')
    
# #     return render(request, 'app/verify_otp.html')


# # # def home(request):
# # #     return render(request, 'app/home.html')
# # def home(request):
# #     if not request.session.get('authenticated'):
# #         return redirect('request_otp')
# #     return render(request, 'app/home.html')
# # # Drug Management Views
# # def drug_list(request):
# #     drugs = Drug.objects.all().order_by('name')
# #     return render(request, 'app/drug_list.html', {'drugs': drugs})

# # def add_drug(request):
# #     if request.method == 'POST':
# #         form = DrugForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, 'Drug added successfully!')
# #             return redirect('drug_list')
# #     else:
# #         form = DrugForm()
    
# #     return render(request, 'app/add_drug.html', {'form': form})
# # views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from django.db.models import Q
# from django.contrib import messages
# from django.views.decorators.http import require_POST
# from django.utils import timezone
# from .models import Drug, Sale, SaleItem, PaymentMethod, OTPVerification, AdminPhoneNumber
# from .forms import DrugForm, SaleForm, SaleItemForm
# from .utils import send_sms
# import requests
# from django.conf import settings
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse

# # def request_otp(request):
# #     """Send OTP to all active admin phone numbers"""
# #     if request.method == 'POST':
# #         # Get all active admin phone numbers
# #         admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
# #         if not admin_phones.exists():
# #             messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
# #             return render(request, 'app/request_otp.html')
        
# #         # Create OTP for each admin phone
# #         otp_entries = []
# #         for admin_phone in admin_phones:
# #             otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
# #             otp_entries.append(otp_entry)
            
# #             # Send SMS
# #             try:
# #                 send_sms(admin_phone.phone_number, f"Your pharmacy login OTP is: {otp_entry.otp_code}")
# #                 print(f"OTP sent to {admin_phone.phone_number}: {otp_entry.otp_code}")  # For debugging
# #             except Exception as e:
# #                 print(f"Failed to send SMS to {admin_phone.phone_number}: {str(e)}")
        
# #         # Store OTP IDs in session for verification
# #         request.session['otp_ids'] = [otp.id for otp in otp_entries]
# #         messages.success(request, f'OTP codes sent to {len(admin_phones)} admin number(s)')
# #         return redirect('verify_otp')
    
# #     return render(request, 'app/request_otp.html')

# # def verify_otp(request):
# #     """Verify OTP from any of the admin phones"""
# #     if request.method == 'POST':
# #         entered_otp = request.POST.get('otp')
# #         otp_ids = request.session.get('otp_ids', [])
        
# #         if not otp_ids:
# #             messages.error(request, 'No OTP request found. Please request a new OTP.')
# #             return redirect('request_otp')
        
# #         # Check if entered OTP matches any of the sent OTPs
# #         valid_otp = None
# #         for otp_id in otp_ids:
# #             try:
# #                 otp_record = OTPVerification.objects.get(id=otp_id)
                
# #                 # Check if OTP is valid and not expired
# #                 if (otp_record.otp_code == entered_otp and 
# #                     not otp_record.is_verified and 
# #                     not otp_record.is_expired()):
# #                     valid_otp = otp_record
# #                     break
# #             except OTPVerification.DoesNotExist:
# #                 continue
        
# #         if valid_otp:
# #             # Mark OTP as verified
# #             valid_otp.is_verified = True
# #             valid_otp.save()
            
# #             # Mark all other OTPs from this session as expired/invalid
# #             OTPVerification.objects.filter(
# #                 id__in=otp_ids
# #             ).exclude(id=valid_otp.id).delete()
            
# #             # Set authentication session
# #             request.session['authenticated'] = True
# #             request.session['authenticated_phone'] = valid_otp.admin_phone.phone_number
            
# #             # Clear OTP session data
# #             if 'otp_ids' in request.session:
# #                 del request.session['otp_ids']
            
# #             messages.success(request, 'Login successful!')
# #             return redirect('home')
# #         else:
# #             messages.error(request, 'Invalid or expired OTP. Please try again.')
    
# #     return render(request, 'app/verify_otp.html')

# # def resend_otp(request):
# #     """Resend OTP to admin phones"""
# #     if request.method == 'POST':
# #         # Clear any existing OTP session
# #         if 'otp_ids' in request.session:
# #             # Delete old OTPs
# #             old_otp_ids = request.session['otp_ids']
# #             OTPVerification.objects.filter(id__in=old_otp_ids).delete()
        
# #         return redirect('request_otp')
    
# #     return redirect('verify_otp')

# # def request_otp(request):
# #     """Handle both OTP request and verification on the same page"""
    
# #     # Handle OTP verification
# #     if request.method == 'POST' and 'otp' in request.POST:
# #         entered_otp = request.POST.get('otp')
# #         otp_ids = request.session.get('otp_ids', [])
        
# #         if not otp_ids:
# #             messages.error(request, 'No OTP request found. Please request a new OTP.')
# #             return render(request, 'app/request_otp.html')
        
# #         # Check if entered OTP matches any of the sent OTPs
# #         valid_otp = None
# #         for otp_id in otp_ids:
# #             try:
# #                 otp_record = OTPVerification.objects.get(id=otp_id)
                
# #                 # Check if OTP is valid and not expired
# #                 if (otp_record.otp_code == entered_otp and 
# #                     not otp_record.is_verified and 
# #                     not otp_record.is_expired()):
# #                     valid_otp = otp_record
# #                     break
# #             except OTPVerification.DoesNotExist:
# #                 continue
        
# #         if valid_otp:
# #             # Mark OTP as verified
# #             valid_otp.is_verified = True
# #             valid_otp.save()
            
# #             # Mark all other OTPs from this session as expired/invalid
# #             OTPVerification.objects.filter(
# #                 id__in=otp_ids
# #             ).exclude(id=valid_otp.id).delete()
            
# #             # Set authentication session
# #             request.session['authenticated'] = True
# #             request.session['authenticated_phone'] = valid_otp.admin_phone.phone_number
            
# #             # Clear OTP session data
# #             if 'otp_ids' in request.session:
# #                 del request.session['otp_ids']
            
# #             messages.success(request, 'Login successful!')
# #             return redirect('home')
# #         else:
# #             messages.error(request, 'Invalid or expired OTP. Please try again.')
# #             return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
# #     # Handle OTP request
# #     elif request.method == 'POST' and 'send_otp' in request.POST:
# #         # Get all active admin phone numbers
# #         admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
# #         if not admin_phones.exists():
# #             messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
# #             return render(request, 'app/request_otp.html')
        
# #         # Create OTP for each admin phone
# #         otp_entries = []
# #         for admin_phone in admin_phones:
# #             otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
# #             otp_entries.append(otp_entry)
            
# #             # Send SMS
# #             try:
# #                 send_sms(admin_phone.phone_number, f"Your pharmacy login OTP is: {otp_entry.otp_code}")
# #                 print(f"OTP sent to {admin_phone.phone_number}: {otp_entry.otp_code}")  # For debugging
# #             except Exception as e:
# #                 print(f"Failed to send SMS to {admin_phone.phone_number}: {str(e)}")
        
# #         # Store OTP IDs in session for verification
# #         request.session['otp_ids'] = [otp.id for otp in otp_entries]
# #         messages.success(request, f'OTP codes sent to {len(admin_phones)} admin number(s)')
# #         return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
# #     # Handle resend OTP
# #     elif request.method == 'POST' and 'resend_otp' in request.POST:
# #         # Get all active admin phone numbers
# #         admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
# #         if not admin_phones.exists():
# #             messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
# #             return render(request, 'app/request_otp.html')
        
# #         # Delete old OTPs
# #         old_otp_ids = request.session.get('otp_ids', [])
# #         if old_otp_ids:
# #             OTPVerification.objects.filter(id__in=old_otp_ids).delete()
        
# #         # Create new OTP for each admin phone
# #         otp_entries = []
# #         for admin_phone in admin_phones:
# #             otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
# #             otp_entries.append(otp_entry)
            
# #             # Send SMS
# #             try:
# #                 send_sms(admin_phone.phone_number, f"Your pharmacy login OTP is: {otp_entry.otp_code}")
# #                 print(f"OTP resent to {admin_phone.phone_number}: {otp_entry.otp_code}")  # For debugging
# #             except Exception as e:
# #                 print(f"Failed to send SMS to {admin_phone.phone_number}: {str(e)}")
        
# #         # Store new OTP IDs in session
# #         request.session['otp_ids'] = [otp.id for otp in otp_entries]
# #         messages.success(request, f'OTP codes resent to {len(admin_phones)} admin number(s)')
# #         return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
# #     # Check if there are pending OTPs to show the form
# #     otp_ids = request.session.get('otp_ids', [])
# #     show_otp_form = bool(otp_ids)
    
# #     return render(request, 'app/request_otp.html', {'show_otp_form': show_otp_form})


# # You can remove the verify_otp view since it's now handled in request_otp
# # def verify_otp(request):
# #     # This view is no longer needed

# # def resend_otp(request):
# #     """Resend OTP - this can redirect to request_otp with resend flag"""
# #     if request.method == 'POST':
# #         return request_otp(request)  # This will handle the resend logic
# #     return redirect('request_otp')

# # def send_otp_sms(phone_number, otp_code):
# #     """Send OTP SMS using Mnotify API"""
# #     try:
# #         message = f"Your pharmacy admin login OTP is: {otp_code}. This code will expire in 10 minutes. Do not share this code with anyone."
# #         encoded_message = requests.utils.quote(message)
# #         key = ""
# #         sender_id = 'StellaPharm'  # You can change this to your preferred sender ID
        
# #         url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
# #         response = requests.get(url)
        
# #         if response.status_code == 200:
# #             print(f"OTP SMS sent successfully to {phone_number}: {otp_code}")
# #             return True
# #         else:
# #             print(f"Failed to send OTP SMS to {phone_number}. Status: {response.status_code}")
# #             return False
# #     except Exception as e:
# #         print(f"Error sending OTP SMS to {phone_number}: {str(e)}")
# #         return False


# # def request_otp(request):
# #     """Handle both OTP request and verification on the same page"""
    
# #     # Handle OTP verification
# #     if request.method == 'POST' and 'otp' in request.POST:
# #         entered_otp = request.POST.get('otp')
# #         otp_ids = request.session.get('otp_ids', [])
        
# #         if not otp_ids:
# #             messages.error(request, 'No OTP request found. Please request a new OTP.')
# #             return render(request, 'app/request_otp.html')
        
# #         # Check if entered OTP matches any of the sent OTPs
# #         valid_otp = None
# #         for otp_id in otp_ids:
# #             try:
# #                 otp_record = OTPVerification.objects.get(id=otp_id)
                
# #                 # Check if OTP is valid and not expired
# #                 if (otp_record.otp_code == entered_otp and 
# #                     not otp_record.is_verified and 
# #                     not otp_record.is_expired()):
# #                     valid_otp = otp_record
# #                     break
# #             except OTPVerification.DoesNotExist:
# #                 continue
        
# #         if valid_otp:
# #             # Mark OTP as verified
# #             valid_otp.is_verified = True
# #             valid_otp.save()
            
# #             # Mark all other OTPs from this session as expired/invalid
# #             OTPVerification.objects.filter(
# #                 id__in=otp_ids
# #             ).exclude(id=valid_otp.id).delete()
            
# #             # Set authentication session
# #             request.session['authenticated'] = True
# #             request.session['authenticated_phone'] = valid_otp.admin_phone.phone_number
            
# #             # Clear OTP session data
# #             if 'otp_ids' in request.session:
# #                 del request.session['otp_ids']
            
# #             messages.success(request, 'Login successful!')
# #             return redirect('home')
# #         else:
# #             messages.error(request, 'Invalid or expired OTP. Please try again.')
# #             return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
# #     # Handle OTP request
# #     elif request.method == 'POST' and 'send_otp' in request.POST:
# #         # Get all active admin phone numbers
# #         admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
# #         if not admin_phones.exists():
# #             messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
# #             return render(request, 'app/request_otp.html')
        
# #         # Create OTP for each admin phone and send SMS
# #         otp_entries = []
# #         successful_sends = 0
# #         failed_sends = 0
        
# #         for admin_phone in admin_phones:
# #             otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
# #             otp_entries.append(otp_entry)
            
# #             # Send SMS using Mnotify
# #             if send_otp_sms(admin_phone.phone_number, otp_entry.otp_code):
# #                 successful_sends += 1
# #             else:
# #                 failed_sends += 1
        
# #         # Store OTP IDs in session for verification
# #         request.session['otp_ids'] = [otp.id for otp in otp_entries]
        
# #         # Show appropriate message based on SMS sending results
# #         if successful_sends > 0 and failed_sends == 0:
# #             messages.success(request, f'OTP codes sent successfully to {successful_sends} admin number(s)')
# #         elif successful_sends > 0 and failed_sends > 0:
# #             messages.warning(request, f'OTP sent to {successful_sends} number(s), but failed to send to {failed_sends} number(s)')
# #         else:
# #             messages.error(request, 'Failed to send OTP to any admin numbers. Please try again.')
# #             return render(request, 'app/request_otp.html')
        
# #         return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
# #     # Handle resend OTP
# #     elif request.method == 'POST' and 'resend_otp' in request.POST:
# #         # Get all active admin phone numbers
# #         admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
# #         if not admin_phones.exists():
# #             messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
# #             return render(request, 'app/request_otp.html')
        
# #         # Delete old OTPs
# #         old_otp_ids = request.session.get('otp_ids', [])
# #         if old_otp_ids:
# #             OTPVerification.objects.filter(id__in=old_otp_ids).delete()
        
# #         # Create new OTP for each admin phone and send SMS
# #         otp_entries = []
# #         successful_sends = 0
# #         failed_sends = 0
        
# #         for admin_phone in admin_phones:
# #             otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
# #             otp_entries.append(otp_entry)
            
# #             # Send SMS using Mnotify
# #             if send_otp_sms(admin_phone.phone_number, otp_entry.otp_code):
# #                 successful_sends += 1
# #             else:
# #                 failed_sends += 1
        
# #         # Store new OTP IDs in session
# #         request.session['otp_ids'] = [otp.id for otp in otp_entries]
        
# #         # Show appropriate message based on SMS sending results
# #         if successful_sends > 0 and failed_sends == 0:
# #             messages.success(request, f'OTP codes resent successfully to {successful_sends} admin number(s)')
# #         elif successful_sends > 0 and failed_sends > 0:
# #             messages.warning(request, f'OTP resent to {successful_sends} number(s), but failed to send to {failed_sends} number(s)')
# #         else:
# #             messages.error(request, 'Failed to resend OTP to any admin numbers. Please try again.')
        
# #         return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
# #     # Check if there are pending OTPs to show the form
# #     otp_ids = request.session.get('otp_ids', [])
# #     show_otp_form = bool(otp_ids)
    
# #     return render(request, 'app/request_otp.html', {'show_otp_form': show_otp_form})


# # def resend_otp(request):
# #     """Resend OTP - this can redirect to request_otp with resend flag"""
# #     if request.method == 'POST':
# #         return request_otp(request)  # This will handle the resend logic
# #     return redirect('request_otp')
# def send_otp_sms(phone_number, otp_code):
#     """Send OTP SMS using Mnotify API"""
#     try:
#         message = f"Your pharmacy admin login OTP is: {otp_code}. This code will expire in 10 minutes. Do not share this code with anyone."
#         encoded_message = requests.utils.quote(message)
#         key = ""  # Use your actual API key
#         sender_id = 'StellaPharm'
        
#         url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             print(f"SMS sent successfully to {phone_number}")
#             print(f"OTP sent: {otp_code}")  # For debugging
#             return True
#         else:
#             print(f"Failed to send SMS to {phone_number}")
#             print(f"Response status: {response.status_code}")
#             print(f"Response text: {response.text}")
#             return False
#     except Exception as e:
#         print(f"Error sending SMS to {phone_number}: {str(e)}")
#         return False


# def request_otp(request):
#     """Handle both OTP request and verification on the same page"""
    
#     # Handle OTP verification
#     if request.method == 'POST' and 'otp' in request.POST:
#         entered_otp = request.POST.get('otp')
#         otp_ids = request.session.get('otp_ids', [])
        
#         if not otp_ids:
#             messages.error(request, 'No OTP request found. Please request a new OTP.')
#             return render(request, 'app/request_otp.html')
        
#         # Check if entered OTP matches any of the sent OTPs
#         valid_otp = None
#         for otp_id in otp_ids:
#             try:
#                 otp_record = OTPVerification.objects.get(id=otp_id)
                
#                 # Check if OTP is valid and not expired
#                 if (otp_record.otp_code == entered_otp and 
#                     not otp_record.is_verified and 
#                     not otp_record.is_expired()):
#                     valid_otp = otp_record
#                     break
#             except OTPVerification.DoesNotExist:
#                 continue
        
#         if valid_otp:
#             # Mark OTP as verified
#             valid_otp.is_verified = True
#             valid_otp.save()
            
#             # Mark all other OTPs from this session as expired/invalid
#             OTPVerification.objects.filter(
#                 id__in=otp_ids
#             ).exclude(id=valid_otp.id).delete()
            
#             # Set authentication session
#             request.session['authenticated'] = True
#             request.session['authenticated_phone'] = valid_otp.admin_phone.phone_number
            
#             # Clear OTP session data
#             if 'otp_ids' in request.session:
#                 del request.session['otp_ids']
            
#             messages.success(request, 'Login successful!')
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid or expired OTP. Please try again.')
#             return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
#     # Handle OTP request
#     elif request.method == 'POST' and 'send_otp' in request.POST:
#         # Get all active admin phone numbers
#         admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
#         if not admin_phones.exists():
#             messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
#             return render(request, 'app/request_otp.html')
        
#         # Create OTP for each admin phone and send SMS
#         otp_entries = []
#         successful_sends = 0
#         failed_sends = 0
        
#         for admin_phone in admin_phones:
#             otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
#             otp_entries.append(otp_entry)
            
#             # Send SMS using Mnotify
#             if send_otp_sms(admin_phone.phone_number, otp_entry.otp_code):
#                 successful_sends += 1
#             else:
#                 failed_sends += 1
        
#         # Store OTP IDs in session for verification
#         request.session['otp_ids'] = [otp.id for otp in otp_entries]
        
#         # Show appropriate message based on SMS sending results
#         if successful_sends > 0 and failed_sends == 0:
#             messages.success(request, f'OTP codes sent successfully to {successful_sends} admin number(s)')
#         elif successful_sends > 0 and failed_sends > 0:
#             messages.warning(request, f'OTP sent to {successful_sends} number(s), but failed to send to {failed_sends} number(s)')
#         else:
#             messages.error(request, 'Failed to send OTP to any admin numbers. Please try again.')
#             return render(request, 'app/request_otp.html')
        
#         return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
#     # Handle resend OTP
#     elif request.method == 'POST' and 'resend_otp' in request.POST:
#         # Get all active admin phone numbers
#         admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
#         if not admin_phones.exists():
#             messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
#             return render(request, 'app/request_otp.html')
        
#         # Delete old OTPs
#         old_otp_ids = request.session.get('otp_ids', [])
#         if old_otp_ids:
#             OTPVerification.objects.filter(id__in=old_otp_ids).delete()
        
#         # Create new OTP for each admin phone and send SMS
#         otp_entries = []
#         successful_sends = 0
#         failed_sends = 0
        
#         for admin_phone in admin_phones:
#             otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
#             otp_entries.append(otp_entry)
            
#             # Send SMS using Mnotify
#             if send_otp_sms(admin_phone.phone_number, otp_entry.otp_code):
#                 successful_sends += 1
#             else:
#                 failed_sends += 1
        
#         # Store new OTP IDs in session
#         request.session['otp_ids'] = [otp.id for otp in otp_entries]
        
#         # Show appropriate message based on SMS sending results
#         if successful_sends > 0 and failed_sends == 0:
#             messages.success(request, f'OTP codes resent successfully to {successful_sends} admin number(s)')
#         elif successful_sends > 0 and failed_sends > 0:
#             messages.warning(request, f'OTP resent to {successful_sends} number(s), but failed to send to {failed_sends} number(s)')
#         else:
#             messages.error(request, 'Failed to resend OTP to any admin numbers. Please try again.')
        
#         return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
#     # Check if there are pending OTPs to show the form
#     otp_ids = request.session.get('otp_ids', [])
#     show_otp_form = bool(otp_ids)
    
#     return render(request, 'app/request_otp.html', {'show_otp_form': show_otp_form})


# def resend_otp(request):
#     """Resend OTP - this can redirect to request_otp with resend flag"""
#     if request.method == 'POST':
#         return request_otp(request)  # This will handle the resend logic
#     return redirect('request_otp')


# def home(request):
#     """Home view with authentication check"""
#     if not request.session.get('authenticated'):
#         return redirect('request_otp')
    
#     # Get authenticated phone info for display (optional)
#     authenticated_phone = request.session.get('authenticated_phone', 'Unknown')
    
#     context = {
#         'authenticated_phone': authenticated_phone
#     }
#     return render(request, 'app/home.html', context)

# def logout_view(request):
#     """Logout view to clear session"""
#     request.session.flush()
#     messages.success(request, 'You have been logged out successfully.')
#     return redirect('request_otp')

# # Middleware function to clean expired OTPs (call this periodically)
# def cleanup_expired_otps():
#     """Clean up expired OTP records"""
#     from django.utils import timezone
#     expired_otps = OTPVerification.objects.filter(
#         expires_at__lt=timezone.now(),
#         is_verified=False
#     )
#     count = expired_otps.count()
#     expired_otps.delete()
#     return count

# # Your existing views remain the same...
# def drug_list(request):
#     if not request.session.get('authenticated'):
#         return redirect('request_otp')
#     drugs = Drug.objects.all().order_by('name')
#     return render(request, 'app/drug_list.html', {'drugs': drugs})

# def add_drug(request):
#     if not request.session.get('authenticated'):
#         return redirect('request_otp')
#     if request.method == 'POST':
#         form = DrugForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Drug added successfully!')
#             return redirect('drug_list')
#     else:
#         form = DrugForm()
    
#     return render(request, 'app/add_drug.html', {'form': form})

# # ... (rest of your existing views with authentication checks added)
# def edit_drug(request, pk):
#     drug = get_object_or_404(Drug, pk=pk)
    
#     if request.method == 'POST':
#         form = DrugForm(request.POST, instance=drug)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Drug updated successfully!')
#             return redirect('drug_list')
#     else:
#         form = DrugForm(instance=drug)
    
#     return render(request, 'app/edit_drug.html', {'form': form, 'drug': drug})

# # Sales Views
# def create_sale(request):
#     payment_methods = PaymentMethod.objects.all()
    
#     if request.method == 'POST':
#         sale_form = SaleForm(request.POST)
#         if sale_form.is_valid():
#             sale = sale_form.save(commit=False)
#             sale.total_amount = 0  # Will be updated later
#             sale.save()
            
#             # Process items from form data
#             total = 0
#             items = []
#             i = 0
#             while f'drug_{i}' in request.POST:
#                 drug_id = request.POST.get(f'drug_{i}')
#                 quantity = int(request.POST.get(f'quantity_{i}', 1))
                
#                 drug = Drug.objects.get(id=drug_id)
#                 price = drug.price
                
#                 # Create sale item
#                 sale_item = SaleItem(
#                     sale=sale,
#                     drug=drug,
#                     quantity=quantity,
#                     price_at_sale=price
#                 )
#                 sale_item.save()
                
#                 # Update total
#                 total += price * quantity
                
#                 # Reduce stock
#                 drug.stock_quantity -= quantity
#                 drug.save()
                
#                 items.append({
#                     'drug': drug.name,
#                     'quantity': quantity,
#                     'price': price,
#                     'total': price * quantity
#                 })
                
#                 i += 1
            
#             # Update sale total
#             sale.total_amount = total
#             sale.save()
            
#             messages.success(request, 'Sale completed successfully!')
#             return redirect('sale_detail', pk=sale.id)
#     else:
#         sale_form = SaleForm()
    
#     context = {
#         'sale_form': sale_form,
#         'payment_methods': payment_methods,
#         'item_form': SaleItemForm(),
#     }
#     return render(request, 'app/create_sale.html', context)

# def sale_detail(request, pk):
#     sale = get_object_or_404(Sale, pk=pk)
#     items = sale.items.all()
    
#     return render(request, 'app/sale_detail.html', {
#         'sale': sale,
#         'items': items
#     })

# def sale_list(request):
#     sales = Sale.objects.all().order_by('-transaction_date')
#     return render(request, 'app/sale_list.html', {'sales': sales})

# # AJAX Views
# def search_drugs(request):
#     query = request.GET.get('query', '')
#     if len(query) < 2:
#         return JsonResponse({'results': []})
    
#     drugs = Drug.objects.filter(
#         Q(name__icontains=query) | Q(description__icontains=query)
#     ).values('id', 'name', 'price', 'stock_quantity')
    
#     return JsonResponse({'results': list(drugs)})

# def get_drug_info(request, drug_id):
#     drug = get_object_or_404(Drug, pk=drug_id)
#     data = {
#         'id': drug.id,
#         'name': drug.name,
#         'price': float(drug.price),
#         'stock': drug.stock_quantity
#     }
#     return JsonResponse(data)




# def daily_sales(request):
#     """
#     View to display daily sales statistics
#     """
#     # Group sales by date and calculate totals
#     daily_stats = Sale.objects.annotate(
#         date=TruncDate('transaction_date')
#     ).values('date').annotate(
#         total_sales=Sum('total_amount'),
#         num_transactions=Count('id')
#     ).order_by('-date')
    
#     return render(request, 'app/daily_sales.html', {
#         'daily_stats': daily_stats
#     })

# def monthly_sales(request):
#     """
#     View to display monthly sales statistics
#     """
#     from django.db.models.functions import TruncMonth
    
#     # Group sales by month and calculate totals
#     monthly_stats = Sale.objects.annotate(
#         month=TruncMonth('transaction_date')
#     ).values('month').annotate(
#         total_sales=Sum('total_amount'),
#         num_transactions=Count('id')
#     ).order_by('-month')
    
#     return render(request, 'app/monthly_sales.html', {
#         'monthly_stats': monthly_stats
#     })




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncDate, TruncMonth
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import requests

from .models import Drug, Sale, SaleItem, PaymentMethod, OTPVerification, AdminPhoneNumber
from .forms import DrugForm, SaleForm, SaleItemForm


# ========================
# AUTHENTICATION VIEWS
# ========================

def send_otp_sms( otp_code,phone_number="0557782728",):
    """Send OTP SMS using Mnotify API"""
    try:
        message = f"Your pharmacy admin login OTP is: {otp_code}. This code will expire in 10 minutes. Do not share this code with anyone."
        encoded_message = requests.utils.quote(message)
        key = ""
        sender_id = 'Afimpp-Tvet'
        
        url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"SMS sent successfully to {phone_number}")
            print(f"OTP sent: {otp_code}")  # For debugging
            return True
        else:
            print(f"Failed to send SMS to {phone_number}")
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending SMS to {phone_number}: {str(e)}")
        return False


def request_otp(request):
    """Handle both OTP request and verification on the same page"""
    
    # Handle OTP verification
    if request.method == 'POST' and 'otp' in request.POST:
        entered_otp = request.POST.get('otp')
        otp_ids = request.session.get('otp_ids', [])
        
        if not otp_ids:
            messages.error(request, 'No OTP request found. Please request a new OTP.')
            return render(request, 'app/request_otp.html')
        
        # Check if entered OTP matches any of the sent OTPs
        valid_otp = None
        for otp_id in otp_ids:
            try:
                otp_record = OTPVerification.objects.get(id=otp_id)
                
                # Check if OTP is valid and not expired
                if (otp_record.otp_code == entered_otp and 
                    not otp_record.is_verified and 
                    not otp_record.is_expired()):
                    valid_otp = otp_record
                    break
            except OTPVerification.DoesNotExist:
                continue
        
        if valid_otp:
            # Mark OTP as verified
            valid_otp.is_verified = True
            valid_otp.save()
            
            # Mark all other OTPs from this session as expired/invalid
            OTPVerification.objects.filter(
                id__in=otp_ids
            ).exclude(id=valid_otp.id).delete()
            
            # Set authentication session
            request.session['authenticated'] = True
            request.session['authenticated_phone'] = valid_otp.admin_phone.phone_number
            
            # Clear OTP session data
            if 'otp_ids' in request.session:
                del request.session['otp_ids']
            
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
    # Handle OTP request
    elif request.method == 'POST' and 'send_otp' in request.POST:
        admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        print(f"Phone number {admin_phones}")
        
        if not admin_phones.exists():
            messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
            return render(request, 'app/request_otp.html')
        
        # Create OTP for each admin phone and send SMS
        otp_entries = []
        successful_sends = 0
        failed_sends = 0
        
        for admin_phone in admin_phones:
            otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
            otp_entries.append(otp_entry)
            
            # Send SMS using Mnotify
            if send_otp_sms(admin_phone.phone_number, otp_entry.otp_code):
                successful_sends += 1
            else:
                failed_sends += 1
        
        # Store OTP IDs in session for verification
        request.session['otp_ids'] = [otp.id for otp in otp_entries]
        
        # Show appropriate message based on SMS sending results
        if successful_sends > 0 and failed_sends == 0:
            messages.success(request, f'OTP codes sent successfully to {successful_sends} admin number(s)')
        elif successful_sends > 0 and failed_sends > 0:
            messages.warning(request, f'OTP sent to {successful_sends} number(s), but failed to send to {failed_sends} number(s)')
        else:
            messages.error(request, 'Failed to send OTP to any admin numbers. Please try again.')
            return render(request, 'app/request_otp.html')
        
        return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
    # Handle resend OTP
    elif request.method == 'POST' and 'resend_otp' in request.POST:
        admin_phones = AdminPhoneNumber.objects.filter(is_active=True)
        
        if not admin_phones.exists():
            messages.error(request, 'No admin phone numbers configured. Please contact administrator.')
            return render(request, 'app/request_otp.html')
        
        # Delete old OTPs
        old_otp_ids = request.session.get('otp_ids', [])
        if old_otp_ids:
            OTPVerification.objects.filter(id__in=old_otp_ids).delete()
        
        # Create new OTP for each admin phone and send SMS
        otp_entries = []
        successful_sends = 0
        failed_sends = 0
        
        for admin_phone in admin_phones:
            otp_entry = OTPVerification.objects.create(admin_phone=admin_phone)
            otp_entries.append(otp_entry)
            
            # Send SMS using Mnotify
            if send_otp_sms(admin_phone.phone_number, otp_entry.otp_code):
                successful_sends += 1
            else:
                failed_sends += 1
        
        # Store new OTP IDs in session
        request.session['otp_ids'] = [otp.id for otp in otp_entries]
        
        # Show appropriate message based on SMS sending results
        if successful_sends > 0 and failed_sends == 0:
            messages.success(request, f'OTP codes resent successfully to {successful_sends} admin number(s)')
        elif successful_sends > 0 and failed_sends > 0:
            messages.warning(request, f'OTP resent to {successful_sends} number(s), but failed to send to {failed_sends} number(s)')
        else:
            messages.error(request, 'Failed to resend OTP to any admin numbers. Please try again.')
        
        return render(request, 'app/request_otp.html', {'show_otp_form': True})
    
    # Check if there are pending OTPs to show the form
    otp_ids = request.session.get('otp_ids', [])
    show_otp_form = bool(otp_ids)
    
    return render(request, 'app/request_otp.html', {'show_otp_form': show_otp_form})


def resend_otp(request):
    """Resend OTP - redirects to request_otp with resend flag"""
    if request.method == 'POST':
        return request_otp(request)
    return redirect('request_otp')


def logout_view(request):
    """Logout view to clear session"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('request_otp')


# ========================
# AUTHENTICATION DECORATORS
# ========================

def login_required(view_func):
    """Decorator to check if user is authenticated"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('authenticated'):
            return redirect('request_otp')
        return view_func(request, *args, **kwargs)
    return wrapper


# ========================
# MAIN VIEWS
# ========================

@login_required
def home(request):
    """Home view with authentication check"""
    authenticated_phone = request.session.get('authenticated_phone', 'Unknown')
    context = {
        'authenticated_phone': authenticated_phone
    }
    return render(request, 'app/home.html', context)


# ========================
# DRUG MANAGEMENT VIEWS
# ========================

@login_required
def drug_list(request):
    """Display list of all drugs"""
    drugs = Drug.objects.all().order_by('name')
    return render(request, 'app/drug_list.html', {'drugs': drugs})


@login_required
def add_drug(request):
    """Add a new drug to inventory"""
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug added successfully!')
            return redirect('drug_list')
    else:
        form = DrugForm()
    
    return render(request, 'app/add_drug.html', {'form': form})


@login_required
def edit_drug(request, pk):
    """Edit an existing drug"""
    drug = get_object_or_404(Drug, pk=pk)
    
    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug updated successfully!')
            return redirect('drug_list')
    else:
        form = DrugForm(instance=drug)
    
    return render(request, 'app/edit_drug.html', {'form': form, 'drug': drug})


# ========================
# SALES MANAGEMENT VIEWS
# ========================

@login_required
def create_sale(request):
    """Create a new sale transaction"""
    payment_methods = PaymentMethod.objects.all()
    
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.total_amount = 0  # Will be updated later
            sale.save()
            
            # Process items from form data
            total = 0
            i = 0
            while f'drug_{i}' in request.POST:
                drug_id = request.POST.get(f'drug_{i}')
                quantity = int(request.POST.get(f'quantity_{i}', 1))
                
                drug = Drug.objects.get(id=drug_id)
                price = drug.price
                
                # Create sale item
                sale_item = SaleItem(
                    sale=sale,
                    drug=drug,
                    quantity=quantity,
                    price_at_sale=price
                )
                sale_item.save()
                
                # Update total
                total += price * quantity
                
                # Reduce stock
                drug.stock_quantity -= quantity
                drug.save()
                
                i += 1
            
            # Update sale total
            sale.total_amount = total
            sale.save()
            
            messages.success(request, 'Sale completed successfully!')
            return redirect('sale_detail', pk=sale.id)
    else:
        sale_form = SaleForm()
    
    context = {
        'sale_form': sale_form,
        'payment_methods': payment_methods,
        'item_form': SaleItemForm(),
    }
    return render(request, 'app/create_sale.html', context)


@login_required
def sale_detail(request, pk):
    """Display details of a specific sale"""
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    
    return render(request, 'app/sale_detail.html', {
        'sale': sale,
        'items': items
    })


@login_required
def sale_list(request):
    """Display list of all sales"""
    sales = Sale.objects.all().order_by('-transaction_date')
    return render(request, 'app/sale_list.html', {'sales': sales})


# ========================
# REPORTING VIEWS
# ========================

@login_required
def daily_sales(request):
    """Display daily sales statistics"""
    daily_stats = Sale.objects.annotate(
        date=TruncDate('transaction_date')
    ).values('date').annotate(
        total_sales=Sum('total_amount'),
        num_transactions=Count('id')
    ).order_by('-date')
    
    return render(request, 'app/daily_sales.html', {
        'daily_stats': daily_stats
    })


@login_required
def monthly_sales(request):
    """Display monthly sales statistics"""
    monthly_stats = Sale.objects.annotate(
        month=TruncMonth('transaction_date')
    ).values('month').annotate(
        total_sales=Sum('total_amount'),
        num_transactions=Count('id')
    ).order_by('-month')
    
    return render(request, 'app/monthly_sales.html', {
        'monthly_stats': monthly_stats
    })


# ========================
# AJAX/API VIEWS
# ========================

@login_required
def search_drugs(request):
    """AJAX endpoint for drug search"""
    query = request.GET.get('query', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    drugs = Drug.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).values('id', 'name', 'price', 'stock_quantity')
    
    return JsonResponse({'results': list(drugs)})


@login_required
def get_drug_info(request, drug_id):
    """AJAX endpoint to get drug information"""
    drug = get_object_or_404(Drug, pk=drug_id)
    data = {
        'id': drug.id,
        'name': drug.name,
        'price': float(drug.price),
        'stock': drug.stock_quantity
    }
    return JsonResponse(data)


# ========================
# UTILITY FUNCTIONS
# ========================

def cleanup_expired_otps():
    """Clean up expired OTP records - call this periodically"""
    expired_otps = OTPVerification.objects.filter(
        expires_at__lt=timezone.now(),
        is_verified=False
    )
    count = expired_otps.count()
    expired_otps.delete()
    return count


def test_sms_connection(phone_number="0557782728"):
    """Test SMS functionality - for debugging purposes only"""
    if not settings.DEBUG:
        return False
    
    test_message = "Test message from Pharmacy Management System"
    encoded_message = requests.utils.quote(test_message)
    key = ""
    sender_id = 'StellaPharm'
    
    url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Test SMS sent successfully")
            return True
        else:
            print(f"Failed to send test SMS: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error testing SMS: {str(e)}")
        return False