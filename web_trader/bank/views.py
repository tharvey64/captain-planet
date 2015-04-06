from django.shortcuts import render, redirect
from django.views.generic import View
from users.models import User
from accounts.models import Account
from bank.models import BankClient, BankAccount

# Create your views here.
class ViewNewClient(View):
	template = 'bank/new_client.html'

	def get(self,request):
		current_user = request.session['user_id']
		user = User.objects.filter(id=current_user)
		return render(request, self.template, {'user':user})

	def post(self, request):
		current_user = request.session['user_id']
		user = User.objects.filter(id=current_user)
		new_client = BankClient(user=user[0])
		new_client.save()
		return redirect('/bank/')

class ViewIndex(View):
	template = 'bank/welcome.html'

	def get(self,request):
		bank_client = BankClient.objects.filter(user__pk=request.session['user_id'])
		if len(bank_client) == 1:
			request.session['bank_client_id'] = bank_client[0].id
			return render(request, self.template, {'user': bank_client[0].user})
		return redirect('new_client/')

class ViewAccount(View):
	template = 'bank/accounts.html'

	def get(self, request):
		info = BankAccount.objects.filter(client__pk = request.session['bank_client_id'])
		return render(request, self.template, {'bank_client':info})

class ViewBanker(View):
	template = 'bank/banker.html'

	def get(self, request):
		return render(request, self.template)

	def post(self, request):
		new_account = Account()
		new_account.save()
		new_b_account = BankAccount(account=new_account)
		new_b_account.type_of = request.POST['type_of']
		bank_client = BankClient.objects.get(id=request.session['bank_client_id'])
		new_b_account.client = bank_client
		new_b_account.save()
		return redirect('/bank/')

class ViewWithdraw(View):
	template = 'bank/withdraw.html'

	def get(self, request):
		info = BankAccount.objects.filter(client__pk=request.session['bank_client_id'])
		return render(request, self.template, {'accounts': info})

	def post(self, request):
		account = BankAccount.objects.filter(account__number=request.POST['account'])
		account[0].account.withdraw(int(request.POST['amount']))
		return redirect('/bank/')

class ViewDeposit(View):
	template = 'bank/deposit.html'

	def get(self, request):
		info = BankAccount.objects.filter(client__pk=request.session['bank_client_id'])
		return render(request, self.template, {'accounts': info})

	def post(self, request):
		account = BankAccount.objects.filter(account__number=request.POST['account'])
		account[0].account.deposit(int(request.POST['amount']))
		return redirect('/bank/')

class ViewTransfer(View):
	template = 'bank/transfer.html'

	def get(self, request):
		account = Bank
		return render(request, self.template)
