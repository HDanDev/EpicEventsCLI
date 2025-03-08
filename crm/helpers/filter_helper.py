from sqlalchemy.orm import Session
from sqlalchemy import or_, Integer, String, DateTime, Boolean, Float
from datetime import datetime
from crm.helpers.format_helper import FormatHelper

class FilterHelper:
    def __init__(self, db: Session, model):
        """
        Initialize the FilterHelper class.
        
        :param db: SQLAlchemy session
        :param model: SQLAlchemy model
        """
        self.db = db
        self.model = model
        self.format_helper = FormatHelper

    def apply_filter(self, filter_field: str = None, filter_value: str = None):
        """
        Apply filtering and sorting logic to the query.

        :param filter_field: Field to filter by (optional)
        :param filter_value: Value to filter by (optional)
        :return: Query result after filtering and sorting
        """
        query = self.db.query(self.model)

        if filter_value:
            # Check if filter_field is valid
            if filter_field and not hasattr(self.model, filter_field):
                raise ValueError(f"Invalid field: {filter_field}")

            # If filter_field is specified, apply filter only on that field
            if filter_field:
                field = getattr(self.model, filter_field)

                if isinstance(field.property.columns[0].type, String):
                    query = query.filter(field.ilike(f'%{filter_value}%'))
                elif isinstance(field.property.columns[0].type, Integer):
                    try:
                        query = query.filter(field == self.filter_ready_int(filter_value))
                    except ValueError:
                        raise ValueError(f"Invalid integer value for field {filter_field}")
                elif isinstance(field.property.columns[0].type, Float):
                    try:
                        query = query.filter(field == self.filter_ready_float(filter_value))
                    except ValueError:
                        raise ValueError(f"Invalid float value for field {filter_field}")
                elif isinstance(field.property.columns[0].type, Boolean):
                    if filter_value.lower() in ['true', 'false']:
                        query = query.filter(field == (filter_value.lower() == 'true'))
                    else:
                        raise ValueError(f"Invalid boolean value for field {filter_field}")
                elif isinstance(field.property.columns[0].type, DateTime):
                    try:
                        filter_date = self.filter_ready_date(filter_value)
                        query = query.filter(field == filter_date)
                    except ValueError:
                        raise ValueError(f"Invalid date format for {filter_field}. Expected format: DD/MM/YYYY-HHhMM")
                else:
                    raise ValueError(f"Unsupported field type for filtering: {filter_field}")

            else:
                # If no field is provided, apply filter across only compatible fields
                filters = []
                # String filters
                for column in self.model.__table__.columns:
                    if isinstance(column.type, String):
                        filters.append(getattr(self.model, column.name).ilike(f'%{filter_value}%'))

                # Integer filters
                for column in self.model.__table__.columns:
                    if isinstance(column.type, Integer):
                        try:
                            filters.append(getattr(self.model, column.name) == self.filter_ready_int(filter_value))
                        except ValueError:
                            continue

                # Float filters
                for column in self.model.__table__.columns:
                    if isinstance(column.type, Float):
                        try:
                            filters.append(getattr(self.model, column.name) == self.filter_ready_float(filter_value))
                        except ValueError:
                            continue

                # Date filters
                for column in self.model.__table__.columns:
                    if isinstance(column.type, DateTime):
                        try:
                            filters.append(getattr(self.model, column.name) == self.filter_ready_date(filter_value))
                        except ValueError:
                            continue

                # Boolean filters
                for column in self.model.__table__.columns:
                    if isinstance(column.type, Boolean):
                        if filter_value.lower() in ['true', 'false']:
                            filters.append(getattr(self.model, column.name) == (filter_value.lower() == 'true'))

                # Apply the filters only to compatible fields
                if filters:
                    query = query.filter(or_(*filters))

        # Sorting if filter_field is provided
        if filter_field:
            field = getattr(self.model, filter_field)
            query = query.order_by(field)

        return query.all()

    def filter_ready_date(self, date):
        """Format and parse date for filtering."""
        try:
            striped_date = datetime.strptime(date.strip(), "%d/%m/%Y-%Hh%M")
            return self.format_helper.format_date(striped_date)
        except ValueError:
            raise ValueError("Invalid date format. Expected format: DD/MM/YYYY-HHhMM")
        
    def filter_ready_int(self, value: str) -> int:
        """Safely convert a string to an integer."""
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Value '{value}' is not a valid integer.")
        
    def filter_ready_float(self, value: str) -> float:
        """Safely convert a string to a float."""
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Value '{value}' is not a valid float.")
