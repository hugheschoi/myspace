import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional


DATA_FILE = Path(__file__).with_name("employees.json")


@dataclass
class Employee:
    employee_id: str
    name: str
    gender: str
    age: int
    department: str
    position: str
    phone: str
    salary: float


class HRManagementSystem:
    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        self.employees: List[Employee] = []
        self.load_data()

    def load_data(self) -> None:
        if not self.data_file.exists():
            self.employees = []
            return

        with self.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        self.employees = [Employee(**item) for item in data]

    def save_data(self) -> None:
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(
                [asdict(employee) for employee in self.employees],
                file,
                ensure_ascii=False,
                indent=2,
            )

    def add_employee(self, employee: Employee) -> bool:
        if self.find_employee(employee.employee_id) is not None:
            return False
        self.employees.append(employee)
        self.save_data()
        return True

    def find_employee(self, employee_id: str) -> Optional[Employee]:
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee
        return None

    def delete_employee(self, employee_id: str) -> bool:
        employee = self.find_employee(employee_id)
        if employee is None:
            return False
        self.employees.remove(employee)
        self.save_data()
        return True

    def update_employee(self, employee_id: str, **updates: object) -> bool:
        employee = self.find_employee(employee_id)
        if employee is None:
            return False

        for field_name, value in updates.items():
            setattr(employee, field_name, value)

        self.save_data()
        return True

    def search_employees(self, keyword: str) -> List[Employee]:
        keyword = keyword.strip().lower()
        return [
            employee
            for employee in self.employees
            if keyword in employee.employee_id.lower()
            or keyword in employee.name.lower()
            or keyword in employee.department.lower()
            or keyword in employee.position.lower()
        ]

    def get_statistics(self) -> dict:
        total = len(self.employees)
        if total == 0:
            return {
                "total": 0,
                "average_salary": 0,
                "departments": {},
            }

        total_salary = sum(employee.salary for employee in self.employees)
        departments: dict[str, int] = {}
        for employee in self.employees:
            departments[employee.department] = departments.get(employee.department, 0) + 1

        return {
            "total": total,
            "average_salary": total_salary / total,
            "departments": departments,
        }


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("输入不能为空，请重新输入。")


def input_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("请输入整数。")


def input_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("请输入数字。")


def input_optional_int(prompt: str, default: int) -> int:
    while True:
        value = input(prompt).strip()
        if not value:
            return default
        try:
            return int(value)
        except ValueError:
            print("请输入整数，或直接回车保留原值。")


def input_optional_float(prompt: str, default: float) -> float:
    while True:
        value = input(prompt).strip()
        if not value:
            return default
        try:
            return float(value)
        except ValueError:
            print("请输入数字，或直接回车保留原值。")


def print_employee_header() -> None:
    print(
        f"{'工号':<12}{'姓名':<10}{'性别':<8}{'年龄':<8}"
        f"{'部门':<12}{'职位':<12}{'电话':<15}{'薪资':<10}"
    )
    print("-" * 87)


def print_employee(employee: Employee) -> None:
    print(
        f"{employee.employee_id:<12}{employee.name:<10}{employee.gender:<8}"
        f"{employee.age:<8}{employee.department:<12}{employee.position:<12}"
        f"{employee.phone:<15}{employee.salary:<10.2f}"
    )


def add_employee_flow(system: HRManagementSystem) -> None:
    print("\n新增员工")
    employee = Employee(
        employee_id=input_non_empty("请输入工号: "),
        name=input_non_empty("请输入姓名: "),
        gender=input_non_empty("请输入性别: "),
        age=input_int("请输入年龄: "),
        department=input_non_empty("请输入部门: "),
        position=input_non_empty("请输入职位: "),
        phone=input_non_empty("请输入电话: "),
        salary=input_float("请输入薪资: "),
    )

    if system.add_employee(employee):
        print("员工添加成功。")
    else:
        print("工号已存在，添加失败。")


def show_all_employees(system: HRManagementSystem) -> None:
    print("\n员工列表")
    if not system.employees:
        print("当前没有员工数据。")
        return

    print_employee_header()
    for employee in system.employees:
        print_employee(employee)


def search_employee_flow(system: HRManagementSystem) -> None:
    keyword = input_non_empty("请输入工号、姓名、部门或职位关键字: ")
    results = system.search_employees(keyword)

    print("\n查询结果")
    if not results:
        print("未找到匹配的员工。")
        return

    print_employee_header()
    for employee in results:
        print_employee(employee)


def update_employee_flow(system: HRManagementSystem) -> None:
    employee_id = input_non_empty("请输入要修改的员工工号: ")
    employee = system.find_employee(employee_id)
    if employee is None:
        print("未找到该员工。")
        return

    print("直接回车表示保留原值。")

    name = input(f"姓名({employee.name}): ").strip() or employee.name
    gender = input(f"性别({employee.gender}): ").strip() or employee.gender

    age = input_optional_int(f"年龄({employee.age}): ", employee.age)

    department = input(f"部门({employee.department}): ").strip() or employee.department
    position = input(f"职位({employee.position}): ").strip() or employee.position
    phone = input(f"电话({employee.phone}): ").strip() or employee.phone

    salary = input_optional_float(f"薪资({employee.salary}): ", employee.salary)

    system.update_employee(
        employee_id,
        name=name,
        gender=gender,
        age=age,
        department=department,
        position=position,
        phone=phone,
        salary=salary,
    )
    print("员工信息修改成功。")


def delete_employee_flow(system: HRManagementSystem) -> None:
    employee_id = input_non_empty("请输入要删除的员工工号: ")
    if system.delete_employee(employee_id):
        print("员工删除成功。")
    else:
        print("未找到该员工。")


def statistics_flow(system: HRManagementSystem) -> None:
    stats = system.get_statistics()
    print("\n统计信息")
    print(f"员工总数: {stats['total']}")
    print(f"平均薪资: {stats['average_salary']:.2f}")
    print("各部门人数:")
    if not stats["departments"]:
        print("暂无部门统计数据。")
        return

    for department, count in stats["departments"].items():
        print(f"- {department}: {count} 人")


def print_menu() -> None:
    print(
        "\n========== 人事管理系统 ==========\n"
        "1. 新增员工\n"
        "2. 查看全部员工\n"
        "3. 查询员工\n"
        "4. 修改员工信息\n"
        "5. 删除员工\n"
        "6. 统计信息\n"
        "0. 退出系统\n"
        "================================"
    )


def main() -> None:
    system = HRManagementSystem(DATA_FILE)

    while True:
        print_menu()
        choice = input("请输入功能编号: ").strip()

        if choice == "1":
            add_employee_flow(system)
        elif choice == "2":
            show_all_employees(system)
        elif choice == "3":
            search_employee_flow(system)
        elif choice == "4":
            update_employee_flow(system)
        elif choice == "5":
            delete_employee_flow(system)
        elif choice == "6":
            statistics_flow(system)
        elif choice == "0":
            print("系统已退出，欢迎下次使用。")
            break
        else:
            print("无效输入，请重新选择。")


if __name__ == "__main__":
    main()
