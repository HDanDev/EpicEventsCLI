import os
from dotenv import load_dotenv
import sentry_sdk


load_dotenv()

SECRET_KEY = os.getenv("APP_SECRET_KEY", "supersecretkey")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crm.db")
KEYRING_SERVICE = os.getenv("KEYRING_SERVICE", "keyringservice")

sentry_sdk.init(
    dsn=os.getenv('SENTRY_URL'),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)