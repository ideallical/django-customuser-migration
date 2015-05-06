from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from project.permissions.base import DefaultPermission


class PermissionMixin(object):
    """
    Check whether an user is authorized to access a view.
    """
    permission_class = DefaultPermission
    permission_instance = None

    loggedin_user = None

    def get_loggedin_user(self):
        """ Return the logged in :class:`~django.contrib.auth.models.User` object. """
        if self.loggedin_user is None:
            self.loggedin_user = self.request.user
        return self.loggedin_user

    def get_context_data(self, **kwargs):
        """ Expose ``loggedin_user`` in the template. """
        context = super(PermissionMixin, self).get_context_data(**kwargs)
        context.update({
            'loggedin_user': self.get_loggedin_user(),
        })
        return context

    def get_permission_instance(self):
        if self.permission_class is None:
            raise NotImplementedError('Implement permission_class.')

        if self.permission_instance is None:
            self.permission_instance = self.permission_class(self.get_loggedin_user())
        return self.permission_instance

    def is_authorized(self, *args, **kwargs):
        return self.get_permission_instance().is_authorized(*args, **kwargs)

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Check for the authorization before passing the request to the standard Django get/post/delete handler.
        """
        # Set earlier to let get_loggedin_user() and get_context_user() work.
        # They run before the get() and post() methods are called.
        self.request = request
        self.args = args
        self.kwargs = kwargs

        # Run checks before entering the view.
        # Note that is_authorized() does not have access to self.object yet,
        # as the normal get() and post() methods are not entered.
        if not self.is_authorized():
            return self.get_permission_instance().response_on_not_authorized(context_instance=RequestContext(request))

        # Give all subclasses a chance to fetch database values that depend on the context user,
        # before entering the global get/post code that does everything. In contrast to overriding get/post, the init()
        # function can call super() first, to let the parent class initialize, and then initialize itself.
        # A get/post function can't run super first, since that would execute the whole view.
        self.init()

        # Run the complete request, returning a response
        return super(PermissionMixin, self).dispatch(request, *args, **kwargs)

    def init(self):
        # Hook to override in subclasses
        pass
