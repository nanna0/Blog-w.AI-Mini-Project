from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Posts, Attachment, Comment, Like
from django.db.models import Q
from .form import CommentForm


# 블로그 구현
# 목록
class PostListView(ListView):
    model = Posts
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    # 게시글 검색
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        user = self.request.user

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()

        if user.is_authenticated:
            queryset = queryset.filter(Q(status="published") | Q(user=user))
        else:
            queryset = queryset.filter(status="published")

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


# 상세
class PostDetailView(DetailView):
    model = Posts
    template_name = "blog/post_detail.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        post = self.get_object()

        # 좋아요 여부 판단
        if self.request.user.is_authenticated:
            context["is_liked"] = post.like.filter(user=self.request.user).exists()
        else:
            context["is_liked"] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            # pk를 넘겨주지 않으면 null로 에러
            comment.posts_id = self.object.pk
            comment.user = request.user
            comment.save()
            return redirect("post_detail", pk=self.object.pk)

        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)


# 생성
class PostCreateView(CreateView):
    model = Posts
    fields = ["title", "content", "status"]
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # 첨부파일 저장
        files = self.request.FILES.getlist("attachments")
        for f in files:
            Attachment.objects.create(posts=self.object, file=f)

        return response


# 수정
class PostUpdateView(UpdateView):
    model = Posts
    fields = ["title", "content", "status"]
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        # 첨부파일 추가
        files = self.request.FILES.getlist("attachments")
        for f in files:
            Attachment.objects.create(posts=self.object, file=f)

        # 첨부파일 삭제
        delete_ids = self.request.POST.getlist("delete_attachments")
        if delete_ids:
            Attachment.objects.filter(id__in=delete_ids, posts=self.object).delete()

        return response


# 삭제
class PostDeleteView(DeleteView):
    model = Posts
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")


# 좋아요 토글
def toggle_like(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs.delete()  # 좋아요 취소
    else:
        Like.objects.create(user=request.user, post=post)  # 좋아요 추가
    return redirect("post_detail", pk=post.id)


# ai 맞춤법
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

@csrf_exempt
def spellcheck_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')

        prompt = f"다음 문장의 맞춤법을 고쳐줘:\n\n{text}"
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            corrected = response.choices[0].message.content.strip()
            return JsonResponse({"corrected_text": corrected})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
