package viewmodel

import (
	"nutri-flow/model"

	"fyne.io/fyne/v2/data/binding"

	"nutri-flow/pkg"
)

// ViewModel for Today's Progress tab

type ProgressViewModel struct {
	Progress             *model.Progress
	CaloriesPercent      binding.String
	ProteinPercent       binding.String
	CarbonhydratePercent binding.String
}

func NewProgressViewModel() *ProgressViewModel {
	progress := &model.Progress{
		GoalCalories:     2000,
		GoalProtein:      200,
		GoalCarbohydrate: 350,
	}
	return &ProgressViewModel{
		Progress:             progress,
		CaloriesPercent:      binding.NewString(),
		ProteinPercent:       binding.NewString(),
		CarbonhydratePercent: binding.NewString(),
	}
}

func (vm *ProgressViewModel) AddProgress(progress model.Progress) {
	vm.Progress.Add(progress)
	vm.CaloriesPercent.Set(pkg.CalculatePercentage(vm.Progress.Calories, vm.Progress.GoalCalories))
	vm.ProteinPercent.Set(pkg.CalculatePercentage(vm.Progress.Protein, vm.Progress.GoalProtein))
	vm.CarbonhydratePercent.Set(pkg.CalculatePercentage(vm.Progress.Carbohydrate, vm.Progress.GoalCarbohydrate))
}
