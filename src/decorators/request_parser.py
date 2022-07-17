from webargs.flaskparser import use_args

def use_args_with(schema_cls, schema_kwargs=None, **kwargs):
    schema_kwargs = schema_kwargs or {}

    def factory(request):
        # Filter based on 'fields' query parameter
        only = request.args.get("fields", None)
        # Respect partial updates for PATCH requests
        partial = request.method == "PATCH"
        return schema_cls(
            only=only, partial=partial, context={"request": request}, **schema_kwargs
        )

    return use_args(factory, **kwargs)
