from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import forms
from . import models

class FixView(TemplateView):
	template_name = 'classapp/fix.html'

class HomeView(TemplateView):
	template_name = 'classapp/home.html'

class LogoutView(TemplateView):
	template_name = 'classapp/home.html'

	def get(self, request):
		if request.session.get('login',False):
			request.session['login'] = False

		return render(request, 'classapp/msg.html',{'msg':"로그아웃 했습니다"})

class LoginView(FormView):
	form_name = forms.LoginForm
	template_name = 'classapp/login.html'
	
	def post(self, request):
		form = forms.LoginForm(request.POST)
		if form.is_valid():
			user_id = form.cleaned_data['user_id']
			user_pw = form.cleaned_data['user_pw']
			
			user_type = -1

			try:
				qs = models.Student.objects.filter(email=user_id,password=user_pw).get()
				user_type = 0
			except:
				try:
					qs = models.Professor.objects.filter(email=user_id,password=user_pw).get()
					user_type = 1
				except:
					try:
						qs = models.Admin.objects.filter(email=user_id,password=user_pw).get()
						user_type = 2
					except:
						return render(request, 'classapp/login.html', {'form':form})

			request.session['login'] = True
			request.session['email'] = qs.email
			request.session['id_code'] = qs.id
			request.session['user_type'] = user_type
			request.session.set_expiry(600)

			return render(request, 'classapp/msg.html',{'msg':"로그인 성공"})
		else:
			return render(request, 'classapp/login.html', {'form':form})
	
	def get(self, request):
		if request.session.get('login',False):
			return render(request, 'classapp/msg.html',{'msg':"이미 로그인 했습니다"})
		form = forms.LoginForm()
		return render(request, 'classapp/login.html', {'form':form})


class MyInfoView(FormView):
	form_name = forms.MyinfoForm
	template_name = 'classapp/myinfo.html' 
	
	def get(self, request, *args, **kwargs):
		form = forms.MyinfoForm()
		if request.session['login']:
			login_id = request.session['id_code']
			user_type = request.session['user_type']
			pass_fix = form['pass_fix']
			number_fix = form['number_fix']
			return render(request, 'classapp/myinfo.html', {'form':form})
		else:
			return render(request, 'classapp/msg.html',{'msg':"다시 로그인 해주세요"})
		return render(request, 'classapp/myinfo.html', {'form':form})
	
	def post(self, request, *args, **kwargs): 
		form = forms.MyinfoForm(request.POST)
		if form.is_valid():
			login_id = request.session['email']
			user_type = request.session['user_type']
			pass_fix = form.cleaned_data['pass_fix']
			number_fix = form.cleaned_data['number_fix']
			if user_type == 0:
				qs = models.Student.objects.filter(email = login_id)
				qs.update(password = pass_fix, number = number_fix)
				return render(request, 'classapp/msg.html',{'msg':"정보가 변경 되었습니다"})
			elif user_type == 1:
				qs = models.Professor.objects.filter(email = login_id)
				qs.update(password = pass_fix, number = number_fix)
				return render(request, 'classapp/msg.html',{'msg':"정보가 변경 되었습니다"})
		return render(request, 'classapp/myinfo.html', {'form':form})

class Registerview_select(FormView):
	form_name = forms.Register_choice
	template_name = 'classapp/register_select.html'

	def get(self, request,*args,**kwargs):
		form = forms.Register_choice()
		return render(request,'classapp/register_select.html',{'form':form})

	def post(self,request,*args,**kwargs):
		form = forms.Register_choice(request.POST)
		if form.is_valid():
			your_choice = form.cleaned_data['choice']
			print(your_choice)
			if your_choice == 'Professor':
				return HttpResponseRedirect(reverse('classapp:register_p'))
			if your_choice == 'Student':
				return HttpResponseRedirect(reverse('classapp:register_s'))
		return render(request,'classapp/register_select.html',{'form':your_choice})

class RegisterView_S(FormView):
	form_name = forms.RegisterForm_S
	template_name = 'classapp/register_s.html' 
	
	def get(self, request, *args, **kwargs):
		form = forms.RegisterForm_S()
		return render(request, 'classapp/register_s.html', {'form':form})

	def post(self, request, *args, **kwargs): 
		form = forms.RegisterForm_S(request.POST)
		if form.is_valid():
			new_email = form.cleaned_data['email_input']
			new_pass_input = form.cleaned_data['pass_input']
			new_number_input = form.cleaned_data['number_input']     
			models.Student.objects.create(email = new_email, password = new_pass_input, number = new_number_input)
			return render(request, 'classapp/msg.html', {'msg':'회원가입 완료'})
		return render(request, 'classapp/register_s.html', {'form':form})
	'''
	def form_valid(self, form):
		return super(MyFormView, self).form_valid(form)
	'''

class RegisterView_P(FormView):
	form_name = forms.RegisterForm_P
	template_name = 'classapp/register_p.html' 
	
	def get(self, request, *args, **kwargs):
		form = forms.RegisterForm_P()
		return render(request, 'classapp/register_p.html' , {'form':form})

	def post(self, request, *args, **kwargs): 
		form = forms.RegisterForm_P(request.POST)
		if form.is_valid():
			new_email = form.cleaned_data['email_input']
			new_pass_input = form.cleaned_data['pass_input']
			new_number_input = form.cleaned_data['number_input']
			models.Professor.objects.create(email = new_email, password = new_pass_input, number = new_number_input)
			return render(request, 'classapp/msg.html', {'msg':'회원가입 완료'})
		return render(request, 'classapp/register_p.html', {'form':form})
	'''
	def form_valid(self, form):
		return super(MyFormView, self).form_valid(form)
	'''


class BoardListView(ListView):
	model = models.Board


class PostListView(ListView):
	model = models.Post

	def get(self, request, *args, **kwargs):
		board_num = kwargs['board_num']
		object_list = models.Post.objects.filter(board=board_num)
		return render(request, 'classapp/post_list.html', {'object_list':object_list,'board_num':board_num})

class PostWriteView(View):
	model = models.Post

	def get(self, request, *args, **kwargs):
		board_num = kwargs['board_num']
		postForm = forms.PostForm()
		return render(request, 'classapp/post_write.html', {'postForm':postForm, 'board_num':board_num})

	def post(self, request, *args, **kwargs):
		# 게시글 작성시 처리해줄 부분
		form = forms.PostForm(request.POST)
		board_num = kwargs['board_num']
		if form.is_valid() and request.session['login']:
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']

			if request.session['user_type'] == 0: #학생이면
				writer_s = models.Student.objects.filter(id=request.session['id_code']).get()
				writer_p = None
			else:
				writer_s = None
				writer_p = models.Professor.objects.filter(id=request.session['id_code']).get()

			board = models.Board.objects.filter(id=board_num).get()

			models.Post.objects.create(title=title, contents=content, board=board,writer_s=writer_s,writer_p=writer_p)
			return HttpResponseRedirect('/classapp/board/%d/' % board_num)

		return render(request, 'classapp/post_write.html', {'postForm':form, 'board_num':board_num})

class PostDetailView(DetailView):
	model = models.Post

	def get(self, request, *args, **kwargs):
		board_num = kwargs['board_num']
		post_num = kwargs['post_num']
		postInfo = models.Post.objects.filter(board=board_num,id=post_num).get()
		# 조회수 늘리는 기능
		postInfo.view_count += 1
		postInfo.save()
		commentList = models.Comment.objects.filter(board=board_num,post=post_num)
		commentForm = forms.CommentForm()
		return render(request, 'classapp/post_detail.html', {'postInfo':postInfo,'board_num':board_num,
			'commentList':commentList,'commentForm':commentForm})

	def post(self, request, *args, **kwargs):
		# 댓글작성버튼 누를시 처리할 내용
		form = forms.CommentForm(request.POST)
		board_num = kwargs['board_num']
		post_num = kwargs['post_num']

		if form.is_valid() and request.session['login']:
			comment = form.cleaned_data['comment_input']

			writer_s = None; writer_p = None
			
			try:
				writer_s = models.Student.objects.filter(email=request.session['email']).get()
			except:
				writer_p = models.Professor.objects.filter(email=request.session['email']).get()

			board = models.Board.objects.filter(id=board_num).get()
			mpost = models.Post.objects.filter(id=post_num).get()

			models.Comment.objects.create(board=board, post=mpost, writer_s=writer_s, writer_p=writer_p, comment=comment)
			return HttpResponseRedirect('/classapp/board/%d/%d' % (board_num,post_num))

		return render(request, 'classapp/post_detail.html', {'postForm':form, 'board_num':board_num})

class CommentDeleteView(View):

	def post(self, request, *args, **kwargs):
		board_num = kwargs['board_num']
		post_num = kwargs['post_num']
		comment_num = kwargs['comment_num']

		if request.session['login']:
			writer_s = None; writer_p = None

			try:
				writer_s = models.Student.objects.filter(email=request.session['email']).get()
			except:
				writer_p = models.Professor.objects.filter(email=request.session['email']).get()

			qs = models.Comment.objects.filter(id=comment_num,writer_s=writer_s,writer_p=writer_p)

			if qs != None:
				qs.delete()

		return HttpResponseRedirect('/classapp/board/%d/%d' % (board_num,post_num))


class PostEditView(View):
	model = models.Post

	def get(self, request, *args, **kwargs):
		board_num = kwargs['board_num']
		post_num = kwargs['post_num']

		if request.session['login']:
			login_id = request.session['id_code']
			mpost = models.Post.objects.filter(id=post_num).get()

			user_check = False

			if mpost.writer_s != None and request.session['user_type'] == 0:
				if mpost.writer_s.id == login_id:
					user_check = True
			elif mpost.writer_p != None and request.session['user_type'] == 1:
				if mpost.writer_p.id == login_id:
					user_check = True
			if not user_check:		
				return render(request,'classapp/msg.html',{'msg':"권한이 없습니다",'link':'/classapp/board/%d/%d' % (board_num,post_num)})

		postForm = forms.PostForm()
		return render(request, 'classapp/post_edit.html', {'postForm':postForm, 'board_num':board_num,'post_num':post_num})

	def post(self, request, *args, **kwargs):
		# 게시글 수정하기 누르면 처리할부분
		form = forms.PostForm(request.POST)
		board_num = kwargs['board_num']
		post_num = kwargs['post_num']
		if form.is_valid() and request.session['login']:
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']

			if request.session['user_type'] == 0: #학생이면
				writer_s = models.Student.objects.filter(id=request.session['id_code']).get()
				writer_p = None
			else:
				writer_s = None
				writer_p = models.Professor.objects.filter(id=request.session['id_code']).get()

			board = models.Board.objects.filter(id=board_num).get()

			mpost = models.Post.objects.filter(id=post_num, board=board).get()
			mpost.title = title
			mpost.contents = content
			mpost.save()
			return HttpResponseRedirect('/classapp/board/%d/%d' % (board_num,post_num))

		return render(request, 'classapp/post_write.html', {'postForm':form, 'board_num':board_num})


class ChatroomListView(ListView):
	model = models.Chatroom

	def get(self, request, *args,**kwargs):
		object_list = models.Chatroom.objects.filter()
		return render(request,'classapp/chat_list.html',{'object_list':object_list})

class ChatcreateListView(ListView):
	model = models.Chatroom
	
	def get(self, request, *args, **kwargs):
		form = forms.ChatForm()
		return render(request,'classapp/chat_create.html',{'form':form})
	def post(self,request):
		form = forms.ChatForm(request.POST)
		if form.is_valid():
			chat_name = form.cleaned_data['name']
			chat_secret = form.cleaned_data['secret']
			chat_password = form.cleaned_data['password']
			new_chatroom = models.Chatroom.objects.create(name = chat_name,secret = chat_secret,password = chat_password)
			object_list = models.Chatroom.objects.all()
			return render(request,'classapp/chat_list.html',{'object_list':object_list})

class ChatRoomView(View):
	model = models.Chatroom

	def get(self, request, *args, **kwargs):
		return render(request, 'classapp/chat_room.html')

	def post(self, request, *args, **kwargs):
		return render(request, 'classapp/fix.html')


class AssignView(FormView):
	form_name = forms.AssignForm
	template_name = 'classapp/assign.html'
		
	def get(self, request, *args, **kwargs):
		form = forms.AssignForm()
		return render(request, 'classapp/assign.html', {'form':form})

	def post(self, request, *args, **kwargs):
		form = forms.AssignForm(request.POST)
		if form.is_valid():
			login_id = request.session['email']
			user_type = request.session['user_type']
			choice_professor = form.cleaned_data['select_professor']
			choice_student= form.cleaned_data['select_student']
			student = models.Student.objects.filter(email = choice_student).get()
			professor = models.Professor.objects.filter(email = choice_professor).get()
			new_Adviser = models.Adviser.objects.create(professor = professor, student = student)
			return render(request, 'classapp/msg.html',{'msg':"배정 되었습니다","link":reverse('classapp:assign')})


class CreateBoardView(View):
	model = models.Board

	def get(self, request, *args, **kwargs):
		return render(request, 'classapp/fix.html')

	def post(self, request, *args, **kwargs):
		return render(request, 'classapp/fix.html')
		
'''
		def form_valid(self,form):
			return render(request,'classapp/chat_create.html',{'form':form})
'''

'''
	********* get방식의 파라미터 전달 방식
	1. 단일 전달
	def get(self, request, board_num):
		return render(request, 'classapp/test2.html', {'board_num':board_num})

		get메소드의 파라미터에 명시적으로 해둔다. url에서 <int:board_num> => def get(..., board_num)

	2. 여러개 한번에 전달
	def get(self, request, *args, **kwargs):
		board_num = kwargs['board_num']
		return render(request, 'classapp/test2.html', {'board_num':board_num})

		1의 방법을 쓸 경우 전달되는 파라미터가 3개,4개 될 경우 혼돈될 수 있다.
		여러개의 파라미터를 kwargs가 딕셔너리형태로 받고 거기서 빼서 사용하는식으로 한다.
	
'''

class GroupCreateView(FormView):
	models = models.Group
	
	def get(self, request, *args, **kwargs):
		form = forms.GroupCreateForm()
		if request.session['login'] and request.session['user_type'] == 2:
			return render(request, 'classapp/group_create.html',{'form':form})
		else :
			return render(request, 'classapp/msg.html',{'msg':'권한이 없습니다'})
	def post(self, request, *args, **kwargs):
		form = forms.GroupCreateForm(request.POST)
		if form.is_valid() :
			name_input = form.cleaned_data['name_input']
			new_Adviser = models.Group.objects.create(group_name = name_input)
			return render(request, 'classapp/msg.html',{'msg':'등록되었습니다'})


class GroupAssignView(FormView):
	models = models.Groupmember

	def get(self, request, *args, **kwargs):
		form = forms.GroupAssignForm()
		if request.session['login'] and request.session['user_type'] == 2:
			return render(request, 'classapp/group_assign.html', {'form': form})
		else:
			return render(request, 'classapp/msg.html', {'msg':'권한이 없습니다'})
	def post(self, request, *args, **kwargs):
		form = forms.GroupAssignForm(request.POST)
		if form.is_valid():
			group_input = form.cleaned_data['select_group']
			student_input = form.cleaned_data['select_member']
			new_member = models.Groupmember.objects.create(group = group_input, student = student_input)
			return render(request, 'classapp/msg.html',{'msg':'등록되었습니다'})

class GroupListView(ListView):
	models = models.Group

	def get(self, request, *args, **kwargs):
		object_list = models.Group.objects.filter()
		member_count_list = []
		for obj in object_list:
			member_count_list.append( (obj,(len(models.Groupmember.objects.filter(group=obj)))))
		return render(request, 'classapp/group_list.html', {'object_list' : object_list, 'member_count_list': member_count_list})