import { CreateAccountForm } from "@/components/create-account-form";

const SignUp = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-2">
      <CreateAccountForm className="max-w-md w-full" />
    </div>
  );
};

export default SignUp;
