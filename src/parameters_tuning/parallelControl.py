import multiprocessing 
import multiprocessing.pool

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess
    
def parallel_call (param_obj):
   param_obj.call_optimization(fitness_class, parameters_list, solution_size, instance)
   return (obj_ga.get_best_individual()[0], obj_ga.get_best_fitness())
