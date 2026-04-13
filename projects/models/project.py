from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=600)
    files = models.ManyToManyField(
        "ProjectFile", blank=True,
        related_name="projects"
    )
    created_at = models.DateField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'projects'
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['-name']
        unique_together = ('name', 'created_at')

    @property
    def count_of_files(self):
        return self.files.count()
