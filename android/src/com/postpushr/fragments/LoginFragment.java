package com.postpushr.fragments;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;

import com.postpushr.R;
import com.postpushr.fragments.SignInFragment.SignInListener;

public class LoginFragment extends Fragment {

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		getActivity().setTitle("Login");
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup parent,
			Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.fragment_login, parent, false);

		Button loginSubmitButton = (Button) view
				.findViewById(R.id.login_submit_button);

		loginSubmitButton.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				// TODO: validate the info with the server
				// Assuming success:
				((SignInListener) getActivity()).moveToHomeFragment(null);
			}
		});

		return view;
	}
}
