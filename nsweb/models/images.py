from nsweb.core import db
from nsweb.models.analyses import CustomAnalysis, TermAnalysis, TopicAnalysis
from nsweb.models.locations import Location
from nsweb.models.genes import Gene
import datetime


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    label = db.Column(db.String(200))
    kind = db.Column(db.String(200))
    description = db.Column(db.Text)
    stat = db.Column(db.String(200))
    image_file = db.Column(db.String(200))
    display = db.Column(db.Boolean)
    download = db.Column(db.Boolean)
    type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.now)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'image'
    }

    @property
    def uncorrected_image_file(self):
        """ Returns an uncorrected version of the filename if one is found. """
        if '_FDR' not in self.image_file:
            return self.image_file
        return self.image_file.split('_FDR')[0] + '.nii.gz'


class TermAnalysisImage(Image):
    __mapper_args__ = {'polymorphic_identity': 'term'}
    term_analysis_id = db.Column(db.Integer, db.ForeignKey(TermAnalysis.id), nullable=True)


class CustomAnalysisImage(Image):
    __mapper_args__ = {'polymorphic_identity': 'custom'}
    custom_analysis_id = db.Column(db.Integer, db.ForeignKey(CustomAnalysis.id), nullable=True)


class LocationImage(Image):
    __mapper_args__ = {'polymorphic_identity': 'location'}
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id), nullable=True)


class TopicAnalysisImage(Image):
    __mapper_args__ = {'polymorphic_identity': 'topic'}
    topic_analysis_id = db.Column(db.Integer, db.ForeignKey(TopicAnalysis.id), nullable=True)


class GeneImage(Image):
    __mapper_args__ = {'polymorphic_identity': 'gene'}
    gene_id = db.Column(db.Integer, db.ForeignKey(Gene.id), nullable=True)
