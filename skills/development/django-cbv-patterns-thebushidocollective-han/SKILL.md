---
name: django-cbv-patterns
description: Use when Django Class-Based Views for building modular, reusable views. Use when creating CRUD operations and complex view logic.
allowed-tools:
  - Bash
  - Read
---

# Django Class-Based Views

Master Django Class-Based Views for building modular, reusable view
logic with proper separation of concerns.

## Generic Views

Use Django's built-in generic views for common patterns.

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only show published posts
        return queryset.filter(published=True).select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = self.get_queryset().count()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().select_related('author').prefetch_related('comments')

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'published']
    template_name = 'posts/create.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'published']
    template_name = 'posts/update.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('post-list')
```

## Built-in Mixins

Leverage Django's built-in mixins for common functionality.

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    login_url = '/login/'
    redirect_field_name = 'next'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        # Custom handling when test fails
        messages.error(self.request, 'You can only edit your own posts')
        return redirect('post-list')

class AdminPostListView(PermissionRequiredMixin, ListView):
    model = Post
    permission_required = 'posts.view_post'
    raise_exception = True  # Return 403 instead of redirect
```

## Custom Mixins

Create reusable mixins for common patterns.

```python
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages

class AuthorRequiredMixin:
    """Ensure the current user is the object's author."""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, 'You do not have permission')
            return redirect('post-list')
        return super().dispatch(request, *args, **kwargs)

class FormMessageMixin:
    """Add success messages to form views."""
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

class AjaxableResponseMixin:
    """Handle AJAX requests differently."""

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'pk': form.instance.pk,
                'success': True
            }
            return JsonResponse(data)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)

# Usage
class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, FormMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_message = 'Post updated successfully'
```

## Method Resolution Order (MRO)

Understand how Django resolves methods in CBVs.

```python
# MRO matters! Order from left to right
class PostUpdateView(
    LoginRequiredMixin,      # Check login first
    AuthorRequiredMixin,     # Then check authorship
    FormMessageMixin,        # Add messages
    UpdateView               # Base view last
):
    model = Post
    fields = ['title', 'content']

# View the MRO
print(PostUpdateView.__mro__)

# Bad example - wrong order
class BadPostUpdateView(
    UpdateView,              # Base view first - wrong!
    LoginRequiredMixin,
    AuthorRequiredMixin
):
    pass  # Mixins won't work correctly

# Override dispatch to control flow
class CustomView(LoginRequiredMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        # Custom logic before any other processing
        if not request.user.is_verified:
            return redirect('verify-email')
        return super().dispatch(request, *args, **kwargs)
```

## Form Handling in CBVs

Advanced form handling patterns.

```python
from django.views.generic.edit import FormView
from django.contrib import messages

class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def get_form_kwargs(self):
        """Pass request to form."""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        """Pre-populate form."""
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
            initial['name'] = self.request.user.name
        return initial

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Message sent!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors')
        return super().form_invalid(form)

# Multiple forms in one view
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserForm(instance=self.request.user)
        if 'profile_form' not in context:
            context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')

        return self.render_to_response(
            self.get_context_data(user_form=user_form, profile_form=profile_form)
        )
```

## When to Use CBVs vs FBVs

Guidelines for choosing between class-based and function-based views.

```python
# Use CBVs for:
# 1. Standard CRUD operations
class PostListView(ListView):
    model = Post

# 2. Reusable view logic
class OwnerRequiredMixin:
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

# 3. Multiple similar views
class UserPostListView(OwnerRequiredMixin, ListView):
    model = Post

class UserDraftListView(OwnerRequiredMixin, ListView):
    model = Post
    queryset = Post.objects.filter(published=False)

# Use FBVs for:
# 1. Simple one-off views
def simple_view(request):
    return render(request, 'simple.html')

# 2. Complex custom logic that doesn't fit CBV patterns
def complex_workflow(request):
    if request.method == 'POST':
        # Complex multi-step logic
        step = request.POST.get('step')
        if step == '1':
            # Process step 1
            pass
        elif step == '2':
            # Process step 2
            pass
    return render(request, 'workflow.html')

# 3. Views that handle multiple models in non-standard ways
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    comments = Comment.objects.filter(post__author=request.user)
    analytics = calculate_analytics(request.user)
    return render(request, 'dashboard.html', {
        'posts': posts,
        'comments': comments,
        'analytics': analytics
    })
```

## Testing CBVs

Comprehensive testing strategies for class-based views.

```python
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

class PostListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_list_view(self):
        request = self.factory.get('/posts/')
        request.user = self.user
        response = PostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_queryset_only_published(self):
        Post.objects.create(title='Published', author=self.user, published=True)
        Post.objects.create(title='Draft', author=self.user, published=False)

        request = self.factory.get('/posts/')
        request.user = self.user
        response = PostListView.as_view()(request)
        self.assertEqual(len(response.context_data['posts']), 1)

    def test_login_required(self):
        request = self.factory.get('/posts/create/')
        request.user = AnonymousUser()
        response = PostCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_author_required(self):
        other_user = User.objects.create_user('other', password='pass')
        post = Post.objects.create(title='Test', author=other_user)

        request = self.factory.get(f'/posts/{post.pk}/edit/')
        request.user = self.user
        response = PostUpdateView.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 302)  # Redirect denied
```

## Advanced Patterns

Complex CBV patterns for production applications.

```python
# Filtering with GET parameters
class PostFilterView(ListView):
    model = Post
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.GET.get('author')
        published = self.request.GET.get('published')

        if author:
            queryset = queryset.filter(author__name__icontains=author)
        if published is not None:
            queryset = queryset.filter(published=published == 'true')

        return queryset

# Dynamic template selection
class PostDetailView(DetailView):
    model = Post

    def get_template_names(self):
        if self.request.user == self.object.author:
            return ['posts/detail_owner.html']
        return ['posts/detail.html']

# JSON response view
from django.http import JsonResponse

class PostJSONView(DetailView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse({
            'id': self.object.id,
            'title': self.object.title,
            'content': self.object.content,
            'author': self.object.author.name
        })

# Conditional form fields
class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/create.html'

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminPostForm
        return UserPostForm

# Multiple object types
from django.views.generic import TemplateView

class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')

        if query:
            context['posts'] = Post.objects.filter(title__icontains=query)
            context['users'] = User.objects.filter(name__icontains=query)
            context['query'] = query

        return context
```

## Pagination in CBVs

Implement sophisticated pagination patterns.

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

class PostListView(ListView):
    model = Post
    paginate_by = 20
    paginate_orphans = 5  # Avoid last page with few items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add custom pagination data
        paginator = context['paginator']
        page_obj = context['page_object']

        # Calculate page range for display
        index = page_obj.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 4 if index <= max_index - 4 else max_index

        context['page_range'] = list(paginator.page_range)[start_index:end_index]
        context['total_pages'] = paginator.num_pages

        return context

# AJAX pagination
class AjaxPostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/list.html'

    def get_template_names(self):
        if self.request.is_ajax():
            return ['posts/partials/post_list.html']
        return [self.template_name]

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            from django.http import JsonResponse
            posts = [
                {
                    'id': post.id,
                    'title': post.title,
                    'author': post.author.name
                }
                for post in context['object_list']
            ]
            return JsonResponse({
                'posts': posts,
                'has_next': context['page_obj'].has_next(),
                'page': context['page_obj'].number
            })
        return super().render_to_response(context, **response_kwargs)

# Infinite scroll pagination
class InfiniteScrollListView(ListView):
    model = Post
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_infinite_scroll'] = True
        return context
```

## Context Data Manipulation

Master advanced context manipulation techniques.

```python
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add related data
        post = self.object
        context['related_posts'] = Post.objects.filter(
            category=post.category
        ).exclude(id=post.id)[:5]

        # Add user-specific data
        if self.request.user.is_authenticated:
            context['has_liked'] = post.likes.filter(
                user=self.request.user
            ).exists()
            context['is_bookmarked'] = post.bookmarks.filter(
                user=self.request.user
            ).exists()

        # Add computed data
        context['reading_time'] = post.calculate_reading_time()
        context['share_url'] = self.request.build_absolute_uri()

        return context

# Multiple context mixins
class AnalyticsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['analytics_enabled'] = True
        context['tracking_id'] = settings.ANALYTICS_ID
        return context

class BreadcrumbMixin:
    breadcrumbs = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context

    def get_breadcrumbs(self):
        return self.breadcrumbs

class PostDetailView(AnalyticsMixin, BreadcrumbMixin, DetailView):
    model = Post
    breadcrumbs = [
        ('Home', '/'),
        ('Posts', '/posts/'),
    ]

    def get_breadcrumbs(self):
        breadcrumbs = super().get_breadcrumbs()
        breadcrumbs.append((self.object.title, None))
        return breadcrumbs
```

## Method Override Patterns

Override specific methods for fine-grained control.

```python
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'category']

    # Control initial form data
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['author'] = self.request.user
        return initial

    # Control form kwargs
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['categories'] = Category.objects.filter(active=True)
        return kwargs

    # Control form class selection
    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminPostForm
        return PostForm

    # Control success URL dynamically
    def get_success_url(self):
        if 'save_and_add' in self.request.POST:
            return reverse('post-create')
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    # Customize form validation
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.ip_address = self.request.META.get('REMOTE_ADDR')

        # Additional validation
        if form.instance.published and not form.instance.content:
            form.add_error('content', 'Published posts must have content')
            return self.form_invalid(form)

        response = super().form_valid(form)

        # Post-save actions
        messages.success(self.request, 'Post created successfully')

        return response

    # Customize form error handling
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below')
        return super().form_invalid(form)

# Override get_object for custom logic
class PostUpdateView(UpdateView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Track view
        obj.views += 1
        obj.save(update_fields=['views'])

        # Check permissions
        if obj.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('You can only edit your own posts')

        return obj

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter based on user
        if not self.request.user.is_staff:
            queryset = queryset.filter(author=self.request.user)

        # Optimize queries
        queryset = queryset.select_related('author', 'category')

        return queryset
```

## Advanced Mixin Composition

Build complex functionality through mixin composition.

```python
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

class SetHeadlineMixin:
    """Add a headline to the context."""
    headline = None

    def get_headline(self):
        return self.headline

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = self.get_headline()
        return context

class SetButtonTextMixin:
    """Add button text to the context."""
    button_text = 'Submit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = self.button_text
        return context

class FormValidMessageMixin:
    """Display success message after form submission."""
    success_message = 'Form submitted successfully'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(form))
        return response

    def get_success_message(self, form):
        return self.success_message

class DeleteConfirmMixin:
    """Require confirmation before deletion."""
    def delete(self, request, *args, **kwargs):
        if not request.POST.get('confirm'):
            messages.warning(request, 'Please confirm deletion')
            return redirect(self.get_success_url())

        messages.success(request, 'Item deleted successfully')
        return super().delete(request, *args, **kwargs)

class StaffRequiredMixin:
    """Require staff user."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AuditMixin:
    """Track creation and updates."""
    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

# Compose multiple mixins
class PostCreateView(
    LoginRequiredMixin,
    SetHeadlineMixin,
    SetButtonTextMixin,
    FormValidMessageMixin,
    AuditMixin,
    CreateView
):
    model = Post
    fields = ['title', 'content']
    headline = 'Create New Post'
    button_text = 'Create Post'
    success_message = 'Post created successfully!'
```

## Search and Filter Views

Implement advanced search and filtering.

```python
from django.db.models import Q
from django.views.generic import ListView

class PostSearchView(ListView):
    model = Post
    template_name = 'posts/search.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['result_count'] = context['paginator'].count
        return context

class PostFilterView(ListView):
    model = Post
    template_name = 'posts/filter.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Author filter
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author_id=author)

        # Date range filter
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        # Published filter
        published = self.request.GET.get('published')
        if published is not None:
            queryset = queryset.filter(published=published == 'true')

        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        allowed_sorts = ['created_at', '-created_at', 'title', '-title', 'views', '-views']
        if sort in allowed_sorts:
            queryset = queryset.order_by(sort)

        return queryset.select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = User.objects.filter(posts__isnull=False).distinct()
        context['filters'] = self.request.GET
        return context
```

## File Upload Views

Handle file uploads with CBVs.

```python
from django.views.generic.edit import FormView
from django.core.files.storage import default_storage

class FileUploadView(FormView):
    template_name = 'upload.html'
    form_class = FileUploadForm
    success_url = '/success/'

    def form_valid(self, form):
        file = form.cleaned_data['file']

        # Save file
        filename = default_storage.save(f'uploads/{file.name}', file)

        # Process file
        self.process_file(filename)

        messages.success(self.request, f'File {file.name} uploaded successfully')
        return super().form_valid(form)

    def process_file(self, filename):
        # Custom file processing logic
        pass

class MultipleFileUploadView(FormView):
    template_name = 'upload_multiple.html'
    form_class = MultipleFileUploadForm
    success_url = '/success/'

    def form_valid(self, form):
        files = self.request.FILES.getlist('files')

        for file in files:
            # Validate file
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                form.add_error('files', f'{file.name} exceeds size limit')
                return self.form_invalid(form)

            # Save file
            filename = default_storage.save(f'uploads/{file.name}', file)

            # Create database record
            FileUpload.objects.create(
                filename=filename,
                original_name=file.name,
                size=file.size,
                uploaded_by=self.request.user
            )

        messages.success(self.request, f'{len(files)} files uploaded successfully')
        return super().form_valid(form)

class ImageUploadView(CreateView):
    model = Image
    fields = ['title', 'image', 'description']
    template_name = 'images/upload.html'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user

        # Validate image
        image = form.cleaned_data['image']
        if image.size > 5 * 1024 * 1024:  # 5MB
            form.add_error('image', 'Image too large')
            return self.form_invalid(form)

        # Process image (resize, thumbnail, etc.)
        form.instance.thumbnail = self.create_thumbnail(image)

        return super().form_valid(form)

    def create_thumbnail(self, image):
        # Thumbnail creation logic
        pass
```

## Performance Optimization

Optimize CBVs for better performance.

```python
class OptimizedPostListView(ListView):
    model = Post
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.select_related(
            'author'
        ).prefetch_related(
            'comments'
        ).only(
            'id', 'title', 'created_at', 'author__name'
        ).filter(
            published=True
        )

# Caching
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')
class CachedPostListView(ListView):
    model = Post

# Conditional caching based on user
class SmartCachedView(ListView):
    model = Post

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Don't cache for authenticated users
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

# ETags for caching
from django.views.decorators.http import condition

def latest_post(request, *args, **kwargs):
    return Post.objects.latest('updated_at').updated_at

def post_etag(request, *args, **kwargs):
    return str(Post.objects.latest('updated_at').updated_at.timestamp())

class PostListView(ListView):
    model = Post

    @method_decorator(condition(etag_func=post_etag, last_modified_func=latest_post))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```

## When to Use This Skill

Use django-cbv-patterns when building modern, production-ready
applications that require
advanced patterns, best practices, and optimal performance.

## API Views with CBVs

Build API endpoints using CBVs without DRF.

```python
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class PostAPIView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(published=True).values(
            'id', 'title', 'content', 'author__name'
        )
        return JsonResponse(list(posts), safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            post = Post.objects.create(
                title=data['title'],
                content=data['content'],
                author=request.user
            )
            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'message': 'Post created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class PostDetailAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.select_related('author').get(pk=pk)
            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.name,
                'created_at': post.created_at.isoformat()
            })
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

    def put(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
            data = json.loads(request.body)

            post.title = data.get('title', post.title)
            post.content = data.get('content', post.content)
            post.save()

            return JsonResponse({'message': 'Post updated successfully'})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

    def delete(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return JsonResponse({'message': 'Post deleted successfully'})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
```

## Wizard and Multi-Step Forms

Implement multi-step form wizards with CBVs.

```python
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

class MultiStepFormMixin:
    """Mixin for multi-step form handling."""

    def get_step(self):
        return int(self.request.GET.get('step', 1))

    def get_session_key(self, step):
        return f'form_data_step_{step}'

    def save_step_data(self, step, data):
        self.request.session[self.get_session_key(step)] = data

    def get_step_data(self, step):
        return self.request.session.get(self.get_session_key(step), {})

    def clear_wizard_data(self):
        for key in list(self.request.session.keys()):
            if key.startswith('form_data_step_'):
                del self.request.session[key]

class UserRegistrationWizard(MultiStepFormMixin, TemplateView):
    template_name = 'registration/wizard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.get_step()

        if step == 1:
            context['form'] = UserBasicInfoForm(initial=self.get_step_data(1))
        elif step == 2:
            context['form'] = UserProfileForm(initial=self.get_step_data(2))
        elif step == 3:
            context['form'] = UserPreferencesForm(initial=self.get_step_data(3))

        context['step'] = step
        context['total_steps'] = 3
        return context

    def post(self, request, *args, **kwargs):
        step = self.get_step()

        if step == 1:
            form = UserBasicInfoForm(request.POST)
            if form.is_valid():
                self.save_step_data(1, form.cleaned_data)
                return redirect(f'{reverse("registration-wizard")}?step=2')

        elif step == 2:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                self.save_step_data(2, form.cleaned_data)
                return redirect(f'{reverse("registration-wizard")}?step=3')

        elif step == 3:
            form = UserPreferencesForm(request.POST)
            if form.is_valid():
                self.save_step_data(3, form.cleaned_data)

                # Create user with all data
                self.create_user()
                self.clear_wizard_data()

                return redirect('registration-complete')

        return self.render_to_response(self.get_context_data(form=form))

    def create_user(self):
        data1 = self.get_step_data(1)
        data2 = self.get_step_data(2)
        data3 = self.get_step_data(3)

        user = User.objects.create_user(
            username=data1['username'],
            email=data1['email'],
            password=data1['password']
        )

        Profile.objects.create(
            user=user,
            bio=data2['bio'],
            avatar=data2['avatar']
        )

        Preferences.objects.create(
            user=user,
            notifications=data3['notifications'],
            privacy=data3['privacy']
        )
```

## Redirect and Success URL Patterns

Master URL redirection strategies.

```python
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    # Static success URL
    success_url = reverse_lazy('post-list')

    # Dynamic success URL based on object
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']

    # Success URL based on form submission button
    def get_success_url(self):
        if 'save_and_continue' in self.request.POST:
            return reverse('post-update', kwargs={'pk': self.object.pk})
        elif 'save_and_add' in self.request.POST:
            return reverse('post-create')
        else:
            return reverse('post-detail', kwargs={'pk': self.object.pk})

class FlexibleRedirectMixin:
    """Redirect to next parameter or default."""

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

class PostDeleteView(FlexibleRedirectMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')
```

## Template and Response Customization

Customize template selection and response rendering.

```python
from django.views.generic import DetailView
from django.http import HttpResponse
from django.template.loader import render_to_string

class PostDetailView(DetailView):
    model = Post

    # Dynamic template selection
    def get_template_names(self):
        # Mobile template
        if self.request.user_agent.is_mobile:
            return ['posts/detail_mobile.html']

        # Owner template
        if self.request.user == self.object.author:
            return ['posts/detail_owner.html']

        # Default template
        return ['posts/detail.html']

class ExportMixin:
    """Add export functionality to views."""

    def render_to_response(self, context, **response_kwargs):
        export_format = self.request.GET.get('format')

        if export_format == 'pdf':
            return self.render_to_pdf(context)
        elif export_format == 'csv':
            return self.render_to_csv(context)
        elif export_format == 'json':
            return self.render_to_json(context)

        return super().render_to_response(context, **response_kwargs)

    def render_to_pdf(self, context):
        # PDF rendering logic
        html = render_to_string(self.template_name, context)
        # Convert to PDF
        return HttpResponse(pdf_content, content_type='application/pdf')

    def render_to_csv(self, context):
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        # Write CSV data
        for obj in context['object_list']:
            writer.writerow([obj.id, obj.title, obj.author.name])

        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        return response

    def render_to_json(self, context):
        from django.http import JsonResponse
        data = [
            {
                'id': obj.id,
                'title': obj.title,
                'author': obj.author.name
            }
            for obj in context['object_list']
        ]
        return JsonResponse(data, safe=False)

class PostListView(ExportMixin, ListView):
    model = Post
```

## Advanced Testing Patterns

Write comprehensive tests for CBVs.

```python
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse

class PostViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user
        )

    def test_list_view_with_factory(self):
        """Test using RequestFactory."""
        request = self.factory.get('/posts/')
        request.user = self.user

        response = PostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_with_client(self):
        """Test using Client."""
        client = Client()
        response = client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_create_view_requires_login(self):
        """Test login requirement."""
        request = self.factory.get('/posts/create/')
        request.user = AnonymousUser()

        response = PostCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_update_view_author_only(self):
        """Test author-only access."""
        other_user = User.objects.create_user('other', password='pass')
        request = self.factory.get(f'/posts/{self.post.pk}/edit/')
        request.user = other_user

        with self.assertRaises(PermissionDenied):
            PostUpdateView.as_view()(request, pk=self.post.pk)

    def test_context_data(self):
        """Test context data."""
        request = self.factory.get('/posts/')
        request.user = self.user

        view = PostListView()
        view.request = request
        view.object_list = Post.objects.all()

        context = view.get_context_data()
        self.assertIn('object_list', context)
        self.assertIn('view', context)

    def test_form_valid(self):
        """Test form submission."""
        data = {
            'title': 'New Post',
            'content': 'Test content'
        }
        request = self.factory.post('/posts/create/', data)
        request.user = self.user

        response = PostCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_queryset_optimization(self):
        """Test query optimization."""
        with self.assertNumQueries(1):
            request = self.factory.get('/posts/')
            request.user = self.user
            response = OptimizedPostListView.as_view()(request)
            list(response.context_data['object_list'])
```

## Django CBV Best Practices

1. **Follow MRO carefully** - Order mixins correctly: permission mixins first,
   then functionality mixins, base view last
2. **Use built-in mixins** - Leverage LoginRequiredMixin, UserPassesTestMixin
   instead of writing custom permission logic
3. **Override get_queryset()** - Customize querysets in get_queryset(), not
   in the class attribute
4. **Use get_context_data()** - Add extra context properly by calling super()
   first
5. **Keep views focused** - Each view should have a single responsibility
6. **Leverage generic views** - Use built-in generic views for CRUD operations
7. **Create custom mixins** - Extract reusable functionality into mixins
8. **Use get_form_kwargs()** - Pass additional data to forms through
   get_form_kwargs()
9. **Optimize queries** - Use select_related and prefetch_related in
   get_queryset()
10. **Test thoroughly** - Use RequestFactory for unit testing views
11. **Use success_url wisely** - Prefer get_success_url() for dynamic URLs
12. **Handle AJAX requests** - Check request.is_ajax() and return appropriate
    responses
13. **Implement proper pagination** - Always paginate large querysets
14. **Cache where appropriate** - Use method decorators for caching expensive
    views
15. **Document mixin order** - Comment why mixins are ordered a certain way

## Django CBV Common Pitfalls

1. **Wrong mixin order** - Incorrect MRO causes mixins to not work or override
   each other incorrectly
2. **Not calling super()** - Forgetting super() breaks the inheritance chain
3. **Hardcoded querysets** - Defining queryset as class attribute instead of
   using get_queryset()
4. **Overusing CBVs** - Using CBVs for simple views that would be clearer as
   functions
5. **Not understanding dispatch()** - Misusing dispatch() method leads to
   unexpected behavior
6. **Ignoring context_object_name** - Templates are less readable without
   proper context names
7. **Mixing concerns** - Putting too much logic in views instead of models or
   forms
8. **Not optimizing queries** - N+1 problems from not using
   select_related/prefetch_related
9. **Testing with client only** - Not unit testing with RequestFactory
10. **Complex inheritance chains** - Too many mixins make code hard to
    understand and debug
11. **Forgetting CSRF protection** - Disabling CSRF without understanding
    security implications
12. **Not handling exceptions** - Not catching DoesNotExist or PermissionDenied
    in custom methods
13. **Incorrect success_url usage** - Using reverse() instead of reverse_lazy()
    in class attributes
14. **Template name conflicts** - Not setting explicit template_name when
    needed
15. **Missing get_object() customization** - Not customizing get_object() for
    permission checks

## Resources

- [Django Class-Based Views Documentation](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Classy Class-Based Views](https://ccbv.co.uk/)
- [Django CBV Inspector](https://ccbv.co.uk/)
- [Django Mixins Documentation](https://docs.djangoproject.com/en/stable/topics/class-based-views/mixins/)
- [Django Forms in CBVs](https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/)
