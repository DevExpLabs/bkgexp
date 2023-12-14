from fastapi import BackgroundTasks
from db.crud.accounting import accounting as accounting_crud


class BackgroundAccounting:
    def __init__(self, background_tasks: BackgroundTasks) -> None:
        self.background_tasks = background_tasks

    def handler(self, db, client, results) -> None:
        for result in results:
            status = "error" not in result
            data = result if "error" in result else result["output"]["timings"]
            accounting_crud.create(db, client, status, **data)

    def run(self, db, client, results) -> None:
        self.background_tasks.add_task(self.handler, db, client, results)
